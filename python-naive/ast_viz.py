from __future__ import annotations
from ast_ import Id, NamedSet, SetBody, Map, ASTNode


class _CodegenContext:
    def __init__(self, indent_string: str):
        self.unique_id = 0
        self.indent = 0
        self.indent_string = indent_string
        self.out: str = ""
        self._print_header()

    def _print_header(self):
        self._println("%% ===== GENERATED CODE =====")
        self._println("")
        self._println("graph TD")
        self._indent()

    def _indent(self):
        self.indent += 1

    def _unindent(self):
        self.indent -= 1

    def _new_id(self) -> str:
        ret = f"_{self.unique_id}"
        self.unique_id += 1
        return ret

    def _println(self, s: str):
        self.out += self.indent_string * self.indent + f"{s}\n"

    def _codegen_btree(self, left, right, label: str) -> str:
        new_id = self._new_id()
        self._println(f"{new_id}{label}")
        left_id = self.codegen(left)
        right_id = self.codegen(right)
        self._println(f"{new_id} --> {left_id}")
        self._println(f"{new_id} --> {right_id}")
        return new_id

    def __str__(self) -> str:
        return self.out

    def codegen(self, ast: ASTNode | str) -> str:
        if type(ast) == str:
            new_id = self._new_id()
            self._println(f"{new_id}{{{{{ast}}}}}")
            return new_id

        if ast is None:
            new_id = self._new_id()
            self._println(f"{new_id}(( ))")
            return new_id

        match ast:
            case NamedSet(id, set_):
                return self._codegen_btree(id, set_, "[NamedSet]")
            case Id(left, right):
                return self._codegen_btree(left, right, "[Id]")
            case SetBody(left, right):
                return self._codegen_btree(left, right, "[SetBody]")
            case Map(left, right):
                return self._codegen_btree(left, right, "[Map]")

        raise SystemError


def ast_viz_mm(ast: ASTNode) -> str:
    c = _CodegenContext("  ")
    c.codegen(ast)
    return c.out
