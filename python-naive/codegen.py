from __future__ import annotations
from ast_ import ASTNode, Id


class TraitCodegen:
    def __init__(self, indent_width: int = 4, minified: bool = False):
        self._indent_width = indent_width
        self._indent = 0
        self._minified = minified
        self.out = ""
        self._scope: None | Id = None

    def indent(self) -> None:
        self._indent += 1

    def unindent(self) -> None:
        self._indent -= 1

    def enter_scope(self, id: Id) -> None:
        if not self._minified:
            self.indent()
        self._scope += id

    def exit_scope(self) -> None:
        if not self._minified:
            self.unindent()
        if self._scope is None:
            raise SystemError
        self._scope = self._scope.remove()

    def codegen(self, ast) -> str:
        self._print_header()
        self._codegen(ast)
        self._print_footer()
        return self.out

    def println(self, s: str):
        self.out += " " * self._indent * self._indent_width + f"{s}\n"

    def print_(self, s: str):
        self.out += s

    def _print_header(self) -> None:
        raise NotImplementedError

    def _print_footer(self) -> None:
        raise NotImplementedError

    def _codegen(self, ast: ASTNode) -> None:
        raise NotImplementedError
