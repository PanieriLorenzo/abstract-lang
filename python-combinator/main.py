from ast_ import Program, TransformContext
from parser_ import parse
from passes.validate_cardinality import validate_cardinality
from passes.annotate_identifiers import annotate_identifiers
from passes.transform_explicit import transform_explicit

if __name__ == "__main__":
    with open("examples/05.aml") as file:
        p = parse(file.read())

        validate_cardinality(p)
        p = transform_explicit(p)
        # p = annotate_identifiers(p)  # type: ignore

        print(p.dumps(indent=2))
