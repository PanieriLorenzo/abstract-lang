from ast_ import *
import re

_empty_expr_re: None = None # TODO

# TODO: these first two can be combined
_empty_set_1_re = re.compile(r'^(?P<id>\w+) ?; ?(?P<rest>.*?$)')
_empty_set_2_re = re.compile(r'^(?P<id>\w+) ?\{ ?\} ?(?P<rest>.*?$)')
_map_re = re.compile(r'^\b(?P<lhs>[\w\. ]+)\b ?-> ?(?P<rhs>[\w\. \-\>]*) ?; ?(?P<rest>.*?$)')


def _parse_id(s: str) -> Id:
    pass

def parse_source(s: str) -> ASTNode:
    print('lel')
    if m := _empty_set_1_re.match(s):
        return SetBody([
            NamedSet(Id(None, m.group('id')),SetBody([])),
            parse_source(m.group('rest'))
        ])
    if m := _empty_set_2_re.match(s):
        return SetBody([
            NamedSet(Id(None, m.group('id')),SetBody([])),
            parse_source(m.group('rest'))
        ])
    if m := _map_re.match(s):
        return SetBody([

        ])


    print(s)
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
        


