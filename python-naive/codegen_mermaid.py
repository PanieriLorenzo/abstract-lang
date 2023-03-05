"""turn the AST back into AML"""
from __future__ import annotations
from ast_ import ASTNode, NamedSet, SetBody, Map, Id
from codegen import TraitCodegen


class _CodegenContext(TraitCodegen):
    def _print_header(self) -> None:
        self.println("%% generated with the python-naive AML compiler")
        self.println("%% ============================================")
        self.println("")
        self.println("graph TD")
        self.indent()

    def _print_footer(self) -> None:
        self.unindent()
        self.println("")

    def _codegen(self, ast: ASTNode) -> None:
        match ast:
            case NamedSet(id, set_):
                if set_.is_empty():
                    self.println(f"{self.id_generator(self._scope + id)}")
                    return
                self.println(f"subgraph {self.id_generator(self._scope + id)}")
                self.enter_scope(id)
                self._codegen(set_)
                self.exit_scope()
                self.println("end")
            case SetBody(left, right):
                self._codegen(left)
                self._codegen(right)
            case Map(_, _):
                ids = list(ast)
                self.print_(self._indent * self._indent_width * " ")
                self._codegen(ids[0])
                for id in ids[1:]:
                    self.print_(" --> ")
                    self._codegen(id)
                self.print_("\n")
            case Id(_, _):
                self.print_(self.id_generator(ast))


def codegen(ast: NamedSet) -> str:
    c = _CodegenContext()
    return c.codegen(ast.set_)
