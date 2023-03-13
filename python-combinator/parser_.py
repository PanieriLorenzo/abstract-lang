import operator
from typing import Callable, Tuple, Any
from dataclasses import dataclass
from parsy import regex, string, seq


class CompilerPanic(Exception):
    """An internal fatal error from which the compiler cannot safely recover"""
    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")


# class SyntaxError(Exception):
#     def __init__(self, msg, content):
#         super().__init__(f"{msg}: {content}")

# tokens
identifier = regex(r"\b\w+\b")
period = string('.')
arrow = string('->')
kw_as = string('as')
open_bracket = string('[')
close_bracket = string(']')
semicolon = string(';')
quotes = string('"')

# TODO: unescape escaped character after parse
string_literal_test = quotes >> regex(r'(?:[^"\\]|\\.)*') << quotes
qualified_identifier_test = seq(identifier << period, identifier)
map_test = seq(identifier << arrow, identifier)

print(qualified_identifier_test.parse("A.A"))
print(string_literal_test.parse('"\\"gneurhsk\\""'))
