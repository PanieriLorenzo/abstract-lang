"""takes a freshly parsed AST and reduces its complexity to the most compact AST"""

from ast_ import ASTNode, NamedSet


class _OptimizerContext:
    def __init__(self) -> None:
        self.ast: ASTNode = None

    def optimize(self, ast: ASTNode):
        match ast:
            case NamedSet(_, _):
                pass


def optimize_ast(ast: ASTNode) -> ASTNode:
    c = _OptimizerContext()
    return c.optimize(ast)
