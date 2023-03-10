"""takes a freshly parsed AST and reduces its complexity to the most compact AST"""
from __future__ import annotations
from ast_ import ASTNode, NamedSet, SetBody


def lower(ast: ASTNode):
    match ast:
        case NamedSet(_, _):
            return ast.dedupe().percolate().expand().normalize()
        case SetBody(_, _):
            return ast.normalize().dedupe()
        case None:
            raise TypeError
        case _:
            return ast
