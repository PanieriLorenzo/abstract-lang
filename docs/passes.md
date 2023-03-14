# Passes

## Pipelines

### Target: Mermaid

1. `validate_cardinality`
1. `generate_symbol_table`
1. `lower_explicit`
1. `lower_dedupe`
1. `lower_identifiers`
1. `lower_string_literals`

## Dependencies

Some passes depend on other passes being executed before them. This information is useful in order to parallelize the passes.

```mermaid
TODO
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

### `generate_symbol_table`

