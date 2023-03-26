from __future__ import annotations
from ast_ import Optional
from dataclasses import dataclass


@dataclass
class CodegenContext:
    """Base class to store the state during codegen"""

    def flush(self):
        self.buffer = ""

    def indent(self):
        self.indent_level += 1

    def unindent(self):
        self.indent_level -= 1

    def write_indent(self):
        self.write(" " * self.indent_width * self.indent_level)

    def write(self, s: str):
        self.buffer += s

    def writeln(self, s: str):
        self.write_indent()
        self.write(s)
        self.write("\n")

    def __init__(self, cc: Optional[CodegenContext] = None, indent_width: int = 2):
        if cc is None:
            self.indent_level: int = 0
            self.buffer = ""
        else:
            self.indent_level = cc.indent_level
            self.buffer = cc.buffer
        self.indent_width = indent_width

    def __enter__(self):
        self.indent()
        return self

    def __exit__(self, *args):
        self.unindent()
