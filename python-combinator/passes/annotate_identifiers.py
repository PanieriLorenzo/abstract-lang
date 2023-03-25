"""un-nest identifiers"""

from ast_ import ASTNode, Program, NamedSet, SetBody, Map, Id


class _AnnotateIdentifiersContext:
    def __init__(self):
        self._current_namespace = Id([])

    def enter_namespace(self, id_: Id):
        """you can pass a namespaced Id to enter multiple layers at once"""
        self._current_namespace += id_

    def exit_namespace(self) -> Id:
        ret, self._current_namespace = self._current_namespace.pop()
        return ret

    def exit_namespaces(self, n: int):
        for _ in range(n):
            self.exit_namespace()

    def visit(self, ast: ASTNode) -> ASTNode:
        match ast:
            case Program(set_):
                return Program(self.visit(set_))  # type: ignore
            case NamedSet(id_, set_, label):
                self.enter_namespace(id_)
                ret = NamedSet(self.visit(id_), self.visit(set_), label)  # type: ignore
                self.exit_namespaces(len(id_))
                return ret
            case SetBody(things_):
                return SetBody([self.visit(t) for t in things_])  # type: ignore
            case Map(ids):
                return Map([self.visit(i) for i in ids])  # type: ignore
            case Id(_, _):
                return ast.make_absolute(self._current_namespace)
            case _:
                raise ValueError


def annotate_identifiers(ast: ASTNode):
    c = _AnnotateIdentifiersContext()
    return c.visit(ast)
