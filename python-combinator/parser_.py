import operator
from typing import Callable, Tuple, Any
from dataclasses import dataclass
from parsy import regex, string, seq, alt, forward_declaration, eof
import sys
import ast_


# non-mandatory whitespace
_ws = regex(r"\s*")

# tokens
_kw_as = string("as")
_quote = string("'")
_op_arrow = string("->")
_op_period = string(".")
_semicolon = string(";")
_open_bracket = string("[")
_close_bracket = string("]")
_comment = regex(r"#.*+").result(None)
_simple_identifier = regex(r"\w+")

escaped_char = regex(r"\\.").map(lambda s: s[1])
unescaped_char = regex(r"[^'\\]")

string_literal = _quote.then(
    (escaped_char | unescaped_char).many().map(lambda s: "".join(s))
).skip(_quote)

qualified_identifier = (
    (_ws >> _simple_identifier).sep_by(_ws >> _op_period, min=1).map(ast_.Id)
)

map_ = qualified_identifier.sep_by(_ws >> _op_arrow, min=2).map(ast_.Map)

named_set = forward_declaration()
_statement = (map_ | named_set).skip(_ws >> _semicolon) | (_ws >> _semicolon).result(
    None
)

set_body = (
    (_statement | (_ws >> _comment))
    .many()
    .map(lambda s: filter(lambda x: x is not None, s))
    .map(list)
    .map(ast_.SetBody)
)

named_set.become(
    seq(
        id_=qualified_identifier,
        set_=_ws.then(_open_bracket)
        .then(set_body)
        .skip(_ws)
        .skip(_close_bracket)
        .optional(),
        label=_ws.then(_kw_as).then(_ws).then(string_literal).optional(),
    ).combine_dict(ast_.NamedSet)
)

program = (set_body << eof).map(ast_.Program)


def parse(s: str) -> ast_.Program:
    return program.parse(s)
