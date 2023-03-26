"""un-nest identifiers"""

from ast_ import (
    ASTNode,
    Program,
    NamedSet,
    SetBody,
    Map,
    Id,
    TransformContext,
)


def annotate_identifiers(p: Program) -> Program:
    c = TransformContext()

    def _annotate_identifiers(ast: ASTNode) -> ASTNode:
        match ast:
            case Program(set_):
                return Program(_annotate_identifiers(set_))  # type: ignore
            case NamedSet(id_, set_, label):
                new_id = _annotate_identifiers(id_)
                c.enter_namespace(id_)
                ret = NamedSet(new_id, _annotate_identifiers(set_), label)  # type: ignore
                c.exit_namespace(len(id_))
                return ret
            case SetBody(things_):
                return SetBody([_annotate_identifiers(t) for t in things_])  # type: ignore # noqa E501
            case Map(_):
                return ast
            case Id(_, _):
                return ast.make_absolute(c.current_namespace)
            case _:
                raise ValueError(ast)

    return _annotate_identifiers(p)  # type: ignore
