from codegen_context import CodegenContext
from ast_ import Program, ASTNode, NamedSet, Id, SetBody, Map
from typing import Optional
import config
from datetime import datetime, timezone
from codegen import SourceBuffer


class NamedSetContext(CodegenContext):
    def __init__(self, id_s: str, label: Optional[str], **kwargs):
        super().__init__(**kwargs)
        self.id_s = id_s
        self.label = label

    def __enter__(self):
        self.write_indent()
        self.writeln(f"{self.id_s} [")
        super().__enter__()
        return self

    def __exit__(self, *args):
        super().__exit__()
        if self.label is not None:
            self.writeln(f"] as '{self.label}';")
            return
        self.writeln("];")


def _codegen_aml(ast: ASTNode) -> SourceBuffer:
    buffer = SourceBuffer()
    match ast:
        case Program(set_):
            buffer.writeline("# !!! Machine-generated code ahead, tread with care !!!")
            buffer.newline()
            buffer.writeline(f"# Generated at {datetime.now(timezone.utc).isoformat()}")
            buffer.writeline(f"# {config.output_header}")
            buffer.newline()
            buffer.writebuf(_codegen_aml(set_))
            return buffer
        case SetBody(things_):
            for t in things_:
                buffer.writebuf(_codegen_aml(t))
            return buffer
        case NamedSet(id_, set_, label):
            # TODO: this can be more concise
            id_s = _codegen_aml(id_)
            buffer.write(f"{id_s.consolidate()} ")
            if len(set_) == 0:
                buffer.write("[]")
                if label is not None:
                    buffer.writeline(f" as '{label}';")
                    return buffer
                buffer.writeline(";")
                return buffer
            buffer.writeline("[")
            buffer.writebuf(_codegen_aml(set_).indent())
            buffer.write("]")
            if label is not None:
                buffer.write(f" as '{label}'")
            buffer.writeline(";")
            return buffer
        case Id(strs, _):
            return buffer.write(".".join(strs))
        case Map(ids):
            return buffer.writeline(
                " -> ".join([_codegen_aml(i).consolidate() for i in ids]) + ";"
            )


def codegen_aml(ast: Program) -> str:
    return _codegen_aml(ast).consolidate_with_trailing_newline()
