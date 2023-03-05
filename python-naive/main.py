from parser_ import parse
from preprocessor import preprocess
from lower import lower
import codegen_mermaid
import codegen_aml
from argparse import ArgumentParser
from pathlib import Path


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-f", "--format", choices=["aml", "mermaid"], default="mermaid")
    args = parser.parse_args()
    if args.output is None:
        out = Path(".") / "build" / (args.input + "." + args.format)
    else:
        out = Path(args.output)

    with open(args.input) as file:
        src = file.read()
    src = preprocess(src)
    ast = lower(parse(src))

    if args.format == "mermaid":
        src = codegen_mermaid.codegen(ast)
    if args.format == "aml":
        src = codegen_aml.codegen(ast)

    out.parents[0].mkdir(parents=True, exist_ok=True)
    with open(out, "w") as file:
        file.write(src)
