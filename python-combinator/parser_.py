import operator
from typing import Callable, Tuple, Any
from dataclasses import dataclass


class CompilerPanic(Exception):
    """An internal fatal error from which the compiler cannot safely recover"""
    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")


# class SyntaxError(Exception):
#     def __init__(self, msg, content):
#         super().__init__(f"{msg}: {content}")


ParserP = Callable[[str], Tuple[Any, str]]


def parse(p: ParserP, s: str) -> Tuple[Any, str]:
    (a, s) = p(s)
    return (a, s)


def any_char() -> ParserP:
    """Generates a parser that matches any character once"""
    return lambda s: (s[0], s[1:])


def char_satisfies_p(predicate: Callable[[str], bool]) -> ParserP:
    """Generates a parser that matches a character with a predicate once"""
    def f(s):
        if not s:
            raise SyntaxError("Empty string")
        if predicate(s[0]):
            return (s[0], s[1:])
        raise SyntaxError("Character does not conform to predicate: " + s[0])
    return f


def one_char(c: str) -> ParserP:
    """Generates a parser that maches a character with a fixed value once"""
    def f(s):
        if s[0] == c:
            return (s[0], s[1:])
        raise SyntaxError(f"Unexpected {s[0]}, expecting {c}")
    return f


def any_digit() -> ParserP:
    """Generates a parser that maches any digit once"""
    def f(s):
        if s[0].isdigit():
            return (s[0], s[1:])
        raise SyntaxError(f"Expected digit, got {s[0]}: " + s)
    return f


def compose(p1: ParserP, p2: ParserP) -> ParserP:
    """Match two parsers in sequence"""
    def f(s):
        (a, s1) = parse(p1, s)
        (b, s2) = parse(p2, s1)
        return ((a, b), s2)
    return f


def any_of_two(p1: ParserP, p2: ParserP) -> ParserP:
    """Matches any of two parsers, the first has priority"""
    def f(s):
        try:
            return p1(s)
        except SyntaxError:
            return p2(s)
    return f


print(parse(any_of_two(any_digit(), one_char('h')), 'hello'))
