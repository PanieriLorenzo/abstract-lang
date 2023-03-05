"""turn the AST back into AML"""
from __future__ import annotations
from ast_ import ASTNode, NamedSet, SetBody, Map, Id
from codegen import TraitCodegen


class _CodegenContext(TraitCodegen):
    def _print_header(self) -> None:
        self.println("# generated with the python-naive AML compiler")
        self.println("# ============================================")
        self.println("")

    def _print_footer(self) -> None:
        self.println("")

    def _codegen(self, ast: ASTNode) -> None:
        match ast:
            case NamedSet(id, set_):
                self.print_(self._indent * self._indent_width * " ")
                self.print_(f"{id.left}")
                if set_.is_empty():
                    self.print_(" {};\n")
                    return
                self.print_(" {\n")
                self.indent()
                self._codegen(set_)
                self.unindent()
                self.println("};")
            case SetBody(left, right):
                self._codegen(left)
                self._codegen(right)
            case Map(_, _):
                ids = list(ast)
                print(ids)
                self.print_(self._indent * self._indent_width * " ")
                self._codegen(ids[0])
                for id in ids[1:]:
                    self.print_(" -> ")
                    self._codegen(id)
                self.print_(";\n")
            case Id(left, right):
                self.print_(f"{left}")
                if right is not None:
                    self.print_(".")
                    self._codegen(right)




def codegen(ast: NamedSet) -> str:
    c = _CodegenContext()
    #return c.codegen(ast.set_.left)
    return c.codegen(ast)
