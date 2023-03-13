import ast_
from parser_ import parse
from passes.validate_cardinality import validate_cardinality

if __name__ == "__main__":
    with open("examples/04.aml") as file:
        p = parse(file.read())

        validate_cardinality(p)

        print(p)
