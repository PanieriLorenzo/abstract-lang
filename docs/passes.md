# Passes

## Pipelines

### Target: Mermaid

1. `parse`
1. `generate_symbol_table`
1. `lower_explicit`
1. `lower_dedupe`
1. `lower_percolate_maps`
1. `lower_expand`
1. `lower_string_literals`
1. `lower_identifiers`
1. `codegen_mermaid`

## Dependencies

Some passes depend on other passes being executed before them. This information is useful in order to parallelize the passes.

```mermaid
graph BT

lower_explicit -> generate_symbol_table -> parse
lower_identifiers -> generate_symbol_table
lower_string_literals -> parse
lower_expand -> generate_symbol_table
lower_dedupe -> generate_symbol_table
```

## Validation Passes

### `validate_cardinality`

A simple sanity check, that ensures there are no nodes with fewer children then the allowed miniumum.

## Lowering Passes

### `lower_identifiers`

Transforms identifiers so that they are compatible with the identifiers allowed in the target language.
If an identifier is transformed and it doesn't have a label, a label is created with the original name.

The transformation has to ensure the uniqueness of identifiers, it may change already valid identifiers in order to
ensure uniqueness.

For example, Mermaid does not have a notion of namespaces, so the identifiers
need to be flattened.

### `lower_explicit`

Makes implicit sets explicit. For example:

```
A -> B;

# becomes
A [];
B [];
A -> B;
```

## Misc Passes

### `parse`

Parse an abstract-lang string. This has some guarantees:
- correct card

### `generate_symbol_table`

Creates a table with all symbols, in a more searchable and un-nested format. Useful to check if a set already exists.
