import operator
from typing import Callable, Tuple, Any
from dataclasses import dataclass
from parsy import regex, string, seq, alt, forward_declaration, eof
import sys
import ast_


class CompilerPanic(Exception):
    """An internal fatal error from which the compiler cannot safely recover"""

    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")


s0 = "# a comment"
s1 = "'lel\\'lol'"
s2 = "foo_bar_baz"
s3 = "foo . bar.baz"
s4 = "A. A ->B .B -> C.C->D"
s5 = " A . A -> B . B ;"
s6 = f"{s5}\n# gneurshk\n{s5}\n;A[A;B;]  ; A as 'a\\''; A;"

# mandatory whitespace
_ws_sep = regex(r"\s+")

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

print(_comment.parse(s0))
print(string_literal.parse(s1))
print(_simple_identifier.parse(s2))
print(qualified_identifier.parse(s3))
print(map_.parse(s4))
print(_statement.parse(s5))
print(program.parse(s6))
