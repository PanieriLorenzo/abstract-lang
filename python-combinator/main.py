from ast_ import Program
from parser_ import parse
from passes.validate_cardinality import validate_cardinality
from passes.annotate_identifiers import annotate_identifiers
from passes.transform_explicit import transform_explicit
from targets.codegen_aml import codegen_aml

if __name__ == "__main__":
    with open("../examples/04.aml") as file:
        p = parse(file.read())

        validate_cardinality(p)
        p = transform_explicit(p)
        p = annotate_identifiers(p)  # type: ignore
        print(codegen_aml(p))

        # print(p.dumps(indent=2))
