# Abstract Lang
A markup language for pure abstractions. The name is temprorary.

## Introduction

Abstract lang is a [markup language]() that can only represent abstract concepts such as sets and mappings. It has some similarity to set theory, but it doesn't strictly follow the rules of any existing set theory. It is mostly useful to represent organizational data, such as diagrams, dependency graphs and data flows.

## Casual Specification

Here follows a casual specification of the language. There is also a formal specification if that's more your thing.

### Sets

The most basic data structure is a set. A set is simply a collection of *things*. Don't worry too much about the exact definition of a thing for now, it is mostly self-evident and a bit akward to strictly define:

```
# a set of things
A { B; C; D; }
```

A set may also be empty, in fact by default all sets are empty and empty sets happen to be extremely useful:

```python
# an empty set
A {}

# a more concise way of writing empty sets
B;
```

All sets must have a name, formally an *identifier*. Identifiers must be unique within a set, but may be reused in different sets (they are scoped).

```
# this inner set A...
Foo { A; }

# ...is different from this inner set A
Bar { B; }

# this is not allowed (actually it is allowed, but will result in A only being added once to the set)
Baz { A; A; }
```

Note that it is not explicitly required for sets to not contain duplicates. For instance, sets will often contain many instances of the empty set.

Now for some notation:

```
# this is a comment

A;    # an empty set called 'A'
B {}  # an empty set called 'B', this notation is also allowed
C { A; B; }   # a set called 'C', which contains two empty sets 'A' and 'B'.

# a very nested set
D { A { A; B; } B { A; B; } }
```

### Maps

A map expresses a relationship between two *things*. 

To map two things, they must have an identifier. Currently, mappings themselves cannot have an identifier, so the only mappings that are possible are between sets.

Notation:
```
A -> B;
A -> B -> C;    # syntax sugar for A -> B; B -> C;
```

A map is also a thing, and thus can be part of a set:

```
A { A -> B; }
```



## Formal Specification

TODO



