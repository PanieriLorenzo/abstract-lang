"""extracts implied sets as a separate definition"""

from ast_ import (
    ASTNode,
    Program,
    NamedSet,
    SetBody,
    Map,
    Id,
)

from itertools import chain


def _transform_explicit(ast: ASTNode) -> ASTNode:
    match ast:
        case Program(set_):
            return Program(_transform_explicit(set_))  # type: ignore
        case NamedSet(id_, set_, label):
            return NamedSet(id_, _transform_explicit(set_), label)  # type: ignore
        case SetBody(things_):
            things_ = [_transform_explicit(t) for t in things_]
            new_sets = chain(
                *[
                    maybe_map.into_sets()
                    for maybe_map in things_
                    if type(maybe_map) == Map
                ]
            )
            things_.extend(new_sets)
            return SetBody(things_)  # type: ignore
        case Map(_) | Id(_, _):
            return ast
        case _:
            raise ValueError(ast)


def transform_explicit(p: Program) -> Program:
    return _transform_explicit(p)  # type: ignore
