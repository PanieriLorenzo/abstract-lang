"""entrypoint for the entire toolchain"""
import re
from typing import Tuple
from ast_ import Id, Map, SetBody, NamedSet


_id_flat_re = re.compile(r"^(\w+)$")
_id_nested_re = re.compile(r"^(?P<lhs>\w+) ?. ?(?P<rest>[\w\. ]+)$")


def _parse_id(s: str) -> Id:
    if _id_flat_re.match(s):
        return Id.flat(s)
    if m := _id_nested_re.match(s):
        return Id(m.group("lhs"), _parse_id(m.group("rest")))
    raise SyntaxError(s)


_map_flat_re = re.compile(r"^(?P<lhs>[\w\. ]+)\b ?-> ?(?P<rhs>[\w\. ]+)$")
_map_nested_re = re.compile(r"^(?P<lhs>[\w\. ]+)\b ?-> ?(?P<rest>.+?)$")


def _parse_map(s: str) -> Map:
    if m := _map_flat_re.match(s):
        return Map(_parse_id(m.group("lhs")), _parse_id(m.group("rhs")))
    if m := _map_nested_re.match(s):
        return Map(_parse_id(m.group("lhs")), _parse_map(m.group("rest")))
    raise SyntaxError


def _nested_brace_helper(s: str) -> Tuple[str, str]:
    """takes a section of code that may contain a "forest" of nested braces
    (the "trees" of this analogy) and splits it into the first tree and the
    remainder of the string. It also "peels off" the top-layer of the first
    tree before returning it.

    ## Examples
    - `"{ a } something { b }"` becomes `"a"`, `"something { b }"`
    - `"{ { a } { b } }"` becomes `"{ a } { b }"`, `""`

    Note that in the second example, there is only one tree in the forest, so
    the remainder string is empty.

    To fully un-nest the braces, this function needs to be used within some
    other recursive function.
    """

    n_braces = 1
    i = 1
    itr = iter(s[1:])
    while True:
        # we start with 1 brace, each time we enter a deeper layer, n_braces
        # is incremented, it can only be 0 if we have exited all layers, in
        # which case, we don't need to get the next character, and we can
        # return the splitted string at the index we got to.
        if n_braces == 0:
            return (s[1: i - 1].strip(), s[i:].strip())

        # if we get here and the string is exhausted, there is no way for
        # n_braces to get to 0, so there must be an unmatched brace
        try:
            c = next(itr)
        except StopIteration:
            raise SyntaxError("dangling brace")
        i += 1

        if c == "{":
            n_braces += 1
            continue
        if c == "}":
            n_braces -= 1
            continue


_empty_statement = re.compile(r"^; ?(?P<rest>.*?)$")
_empty_set_1_re = re.compile(r"^(?P<id>[\w\. ]+)\b ?; ?(?P<rest>.*?)$")
_empty_set_2_re = re.compile(r"^(?P<id>[\w\. ]+)\b ?\{ ?\} ?(?P<rest>.*?)$")
_map_re = re.compile(r"^(?P<map>[\w\. ]+\b(?: ?-> ?\b[\w\. ]+\b)+) ?; ?(?P<rest>.*?)$")

# since this is not a regular language, there will be cases were regexes don't
# work, such as nested sets. We can match the section of unparsable code,
# which in this case is unparsable due to nested braces. The section starts
# at the first occurrance of an open brace and ends at the last occurrance of
# an open brace. This section needs to be parsed with other tools.
_irregular_set_re = re.compile(
    r"^(?P<id>[\w\. ]+)\b ?(?P<irregular>\{ ?.+\}) ?(?P<rest>.*?)$"
)


def _parse_set_body(s: str) -> SetBody:
    if m := _empty_statement.match(s):
        return _parse_set_body(m.group("rest"))
    if (m := _empty_set_1_re.match(s)) or (m := _empty_set_2_re.match(s)):
        return SetBody(
            NamedSet.empty(_parse_id(m.group("id"))), _parse_set_body(m.group("rest"))
        )
    if m := _map_re.match(s):
        return SetBody(_parse_map(m.group("map")), _parse_set_body(m.group("rest")))
    if m := _irregular_set_re.match(s):
        lhs, rhs = _nested_brace_helper(m.group("irregular"))
        return SetBody(
            NamedSet(_parse_id(m.group("id")), _parse_set_body(lhs)),
            _parse_set_body(" ".join([rhs, m.group("rest")]).strip()),
        )
    if len(s.strip()) == 0:
        return SetBody.empty()

    raise SyntaxError(s)


def parse(s: str) -> NamedSet:
    return NamedSet(Id.flat("__main__"), _parse_set_body(s))
