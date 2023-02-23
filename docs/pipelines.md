```mermaid
graph LR

src.aml --> AST --> src.mermaid
AST --> src.graphviz
AST --> src.plantuml
AST --> dict --> src.json
AST --> src.aml
dict --> src.yaml
dict --> src.toml
```