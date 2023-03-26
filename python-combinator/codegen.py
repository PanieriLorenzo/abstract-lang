from __future__ import annotations
import config
from typing import Self


class SourceBuffer:
    def __init__(self):
        self.buffer = [""]

    def write(self, s: str) -> Self:
        """raw write to end of the buffer"""
        self.buffer[-1] += s
        return self

    def newline(self) -> Self:
        """advance buffer to next line"""
        self.buffer.append("")
        return self

    def writeline(self, s: str) -> Self:
        """shorthand for write() followed by newline()"""
        self.write(s)
        self.newline()
        return self

    def writebuf(self, buf: SourceBuffer) -> Self:
        """append another buffer to this"""
        self.buffer.pop()
        buf.buffer.pop()
        self.buffer.extend(buf.buffer)
        self.newline()
        return self

    def indent(self) -> Self:
        """indent every line in the buffer"""
        for i, l in enumerate(self.buffer):
            self.buffer[i] = " " * config.indent_width + l
        return self

    def consolidate(self) -> str:
        return "\n".join(self.buffer)

    def consolidate_with_trailing_newline(self) -> str:
        return "\n".join(self.buffer) + "\n"
