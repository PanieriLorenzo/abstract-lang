```mermaid
graph LR

src.aml --parsing--> AST --lowering--> rich_AST
rich_AST --codegen--> src.mermaid
rich_AST --codegen--> src.graphviz
rich_AST --codegen--> src.plantuml
rich_AST --lowering--> dict --serialization--> src.json
AST --codegen--> src.aml
dict --serialization--> src.yaml
dict --serialization--> src.toml
AST --codegen--> ast_viz.aml
rich_AST --codegen--> namespace_viz.mermaid
```