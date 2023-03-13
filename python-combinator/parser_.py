import operator
from typing import Callable, Tuple, Any
from dataclasses import dataclass
from parsy import regex, string, seq, alt, forward_declaration, eof
import sys


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
s6 = f"{s5}\n# gneurshk\n{s5}\n;A[A;B;]  ; A as 'a'; A;"

# mandatory whitespace
_ws_sep = regex(r"\s+")

# non-mandatory whitespace
_ws = regex(r"\s*")

# tokens
_kw_as = string('as')
_quote = string("'")
_op_arrow = string('->')
_op_period = string('.')
_semicolon = string(';')
_open_bracket = string('[')
_close_bracket = string(']')
_comment = regex(r'#.*+')

string_literal = _quote >> regex(r"(?:[^'\\]|\\.)*") << _quote
simple_identifier = regex(r"\w+")
qualified_identifier = (_ws >> simple_identifier).sep_by(_ws >> _op_period, min=1)
map_ = qualified_identifier.sep_by(_ws >> _op_arrow, min=2)
named_set = forward_declaration()
_statement = (map_ | named_set) << (_ws >> _semicolon) \
           | _ws >> _semicolon
set_body = alt(_statement, _ws >> _comment).at_least(0)
named_set.become(
    seq(qualified_identifier, _ws >> _open_bracket >> set_body, _ws >> _close_bracket >> _ws >> _kw_as >> _ws >> string_literal) |
    seq(qualified_identifier, _ws >> _open_bracket >> set_body << _ws << _close_bracket) |
    seq(qualified_identifier, _ws_sep >> _kw_as >> _ws >> string_literal) |
    seq(qualified_identifier))
program = set_body << eof

print(_comment.parse(s0))
print(string_literal.parse(s1))
print(simple_identifier.parse(s2))
print(qualified_identifier.parse(s3))
print(map_.parse(s4))
print(_statement.parse(s5))
print(program.parse(s6))