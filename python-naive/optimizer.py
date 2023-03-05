"""takes a freshly parsed AST and reduces its complexity to the most compact AST"""
from __future__ import annotations
from ast_ import ASTNode, NamedSet


class _OptimizerContext:
    def __init__(self) -> None:
        self.ast: ASTNode = None

    def optimize(self, ast: ASTNode) -> _OptimizerContext:
        match ast:
            case NamedSet(_, _):
                pass


def optimize_ast(ast: ASTNode) -> ASTNode:
    c = _OptimizerContext().optimize(ast)
    return c.ast
