"""entrypoint for the entire toolchain"""
import re
from ast_ import Id, ASTNode, Map, SetBody, NamedSet


_flat_id_re = re.compile(r'^(\w+)$')


def _parse_id(s: str) -> Id:
    print(s)


_map_inner_re = re.compile(r'^(?P<lhs>[\w\. ]+)\b ?-> ?(?P<rest>.*)$')


def _parse_map(s: str) -> Map:
    if m := _map_inner_re.match(s):
        _parse_id(m.group('lhs'))


_empty_expr_re: None = None    # TODO
_empty_set_1_re = re.compile(r'^(?P<id>\w+) ?; ?(?P<rest>.*?)$')
_empty_set_2_re = re.compile(r'^(?P<id>\w+) ?\{ ?\} ?(?P<rest>.*?)$')
_map_re = re.compile(
    r'^(?P<map>[\w\. ]+\b(?: ?-> ?\b[\w\. ]+\b)+) ?; ?(?P<rest>.*?)$')


def parse_set_body(s: str) -> ASTNode:
    if m := _empty_set_1_re.match(s):
        return SetBody([
            NamedSet(Id(None, m.group('id')),SetBody([])),
            parse_set_body(m.group('rest'))
        ])
    if m := _empty_set_2_re.match(s):
        return SetBody([
            NamedSet(Id(None, m.group('id')),SetBody([])),
            parse_set_body(m.group('rest'))
        ])
    if m := _map_re.match(s):
        return SetBody([
            _parse_map(m.group('map')),
            parse_set_body(m.group('rest'))
        ])
    return None

# def parse(src: ASTNode) -> SetBody:
#     """constructs the AST from source recursively"""

#     match src:
#         # this is always the initial case, when parsing the string
#         # it will yield an AST type which wraps the remaining
#         # unparsed source code, then it will recursively call
#         # parse() on the children.
#         case Source(s):
#             return parse(_parse_source(s))
        

    return SetBody([])
        


