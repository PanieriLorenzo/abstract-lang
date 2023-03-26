from codegen_context import CodegenContext
from ast_ import Program, ASTNode, NamedSet, Id, SetBody, Map
from typing import Optional


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


def _codegen_aml(cc: CodegenContext, ast: ASTNode) -> str:
    match ast:
        case Program(set_):
            return _codegen_aml(cc, set_)
        case SetBody(things_):
            return "".join([_codegen_aml(cc, t) for t in things_])
        case NamedSet(id_, set_, label):
            id_s = _codegen_aml(cc, id_)
            if len(set_) == 0:
                cc.flush()
                cc.write(f"{id_s} []")
                if label is not None:
                    cc.write(f" as '{label}';\n")
                    return cc.buffer
                cc.write(";\n")
                return cc.buffer
            with NamedSetContext(cc=cc, id_s=id_s, label=label) as nsc:
                nsc.writeln("gneurshk;")
                ret = nsc.buffer
            return ret
        case Id(strs, _):
            return ".".join(strs)
        case Map(ids):
            return " -> ".join([_codegen_aml(cc, i) for i in ids]) + ";\n"


def codegen_aml(ast: Program) -> str:
    ic = CodegenContext()
    return _codegen_aml(ic, ast)
