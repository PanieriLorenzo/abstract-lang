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


identifier = regex(r"\b\w+\b")
period = string('.')
qualified_identifier = seq(identifier << period, identifier)

print(qualified_identifier.parse("A.A"))



