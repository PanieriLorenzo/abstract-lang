import ast_
from errors import CompilerPanic


def validate_cardinality(a: ast_.ASTNode):
    """A sanity check that ensures you don't have less than the minimum number
    of members of a collection, for example a map with a single identifier."""

    match a:
        case ast_.Program(set_):
            validate_cardinality(set_)
        case ast_.SetBody(things_):
            for thing in things_:
                validate_cardinality(thing)
        case ast_.NamedSet(id_, set_, _):
            validate_cardinality(id_)
            validate_cardinality(set_)
        case ast_.Map(ids):
            if len(ids) < 2:
                raise CompilerPanic("too few identifiers in map", a)
            for id_ in ids:
                validate_cardinality(id_)
        case ast_.Id(strs):
            if len(strs) < 1:
                raise CompilerPanic("too few words in identifier", a)
