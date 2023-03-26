import pathlib

version = pathlib.Path("VERSION").read_text()
libname = "<libname>"
output_header = f"Generated with {libname}, the official AML package"
indent_width = 2
minified_output = False
