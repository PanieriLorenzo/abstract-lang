"""un-nest identifiers"""

from ast_ import (
    ASTNode,
    Program,
    NamedSet,
    SetBody,
    Map,
    Id,
)

from namespace_context import NamespaceContext


def _annotate_identifiers(nc: NamespaceContext, ast: ASTNode) -> ASTNode:
    match ast:
        case Program(set_):
            return Program(_annotate_identifiers(nc, set_))  # type: ignore
        case NamedSet(id_, set_, label):
            new_id = _annotate_identifiers(nc, id_)
            with NamespaceContext(new_id, nc) as nc:
                ret = NamedSet(new_id, _annotate_identifiers(nc, set_), label)  # type: ignore
            return ret
        case SetBody(things_):
            return SetBody([_annotate_identifiers(nc, t) for t in things_])  # type: ignore # noqa E501
        case Map(_):
            return ast
        case Id(_, _):
            return ast.make_absolute(nc.current_namespace)
        case _:
            raise ValueError(ast)


def annotate_identifiers(p: Program) -> Program:
    return _annotate_identifiers(NamespaceContext.empty(), p)  # type: ignore
