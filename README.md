# Abstract Lang
A markup language for pure abstractions. The name is temprorary.

## Introduction

Abstract lang is a [markup language]() that can only represent abstract concepts such as sets and mappings. It has some similarity to set theory, but it doesn't strictly follow the rules of any existing set theory. It is mostly useful to represent organizational data, such as diagrams, dependency graphs and data flows.

I developed it originally, as I was frustrated with the existing diagram markdown languages like [graphviz](), [mermaid]() and [plantuml]() for their clunkyness, lack of generality and lack of namespaces, but I realized that it may be useful not only for drawing diagrams but as a data representation format.

## Casual Specification

Here follows a casual specification of the language. There is also a formal specification if that's more your thing.

### Sets

The most basic data structure is a set. A set is simply a collection of *things*. Don't worry too much about the exact definition of a thing for now, it is mostly self-evident and a bit akward to strictly define:

```python
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

```python
# this inner set A...
Foo { A; }

# ...is different from this inner set A
Bar { B; }

# this is not allowed (actually it is allowed, but will result in A only being added once to the set)
Baz { A; A; }
```

Note that some rules of set theory here are not strictly required, but naturally arise as a consequence of the syntax and semantics of the language. For example, it is not explicitly required that sets do not contain themselves, but the syntax makes it impossible to represent sets that contain themselves, so they naturally never arise.

### Maps

A map expresses a relationship between two *things*. 

```python
# a map between A and B
A -> B;

# syntax sugar for A -> B; B -> C;
A -> B -> C;
```

A map is also a thing, and thus can be part of a set:

```python
A { A -> B; }
```

A map can also be given a name, but unlike sets, this isn't mandatory:

```python
A -> B: depends_on
```

> TODO: right now a maps name is not really an identifier, so you can't use it for making maps of maps.

You can also map things that are inside a set to things that are inside another set, but you need to use *qualified identifiers* in order to refer to them:

```python
Foo { A; }
Bar { A; }
Foo.A -> Bar.A;
```

Things can get pretty funky when you do very nested things...

```python
A { A { A; B; } B { A; B; } }
B { A { A; B; } B { A; B; } }

A.A.A -> B.A.A;
A.B.A -> A.A.B;
```

And you are also allowed to map something to itself:

```python
A -> A;
```

And you can map a thing to the set that contains it:

```python
A { A; }
A.A -> A;
A -> A.A;
```

Note that it is not possible to place a map inside of a set, if the map contains the set. This arises from the syntax of the language, and isn't explicitly enforced.

You don't need to define the two things a map connects, they are implicitly defined as soon as they are referred to, for example:

```python
# this implies the existence of the sets A and B
A -> B;
```

### Other stuff

There are a couple of other features, that don't have any formal significance, they are purely convenient. 

You can label things with arbitrary strings. These labels are used for example when generating a graphical representation of the data:

```python
# a labelled set
A {} as "any string goes here";

# labelled maps
A -> B as "any string goes here";
C -> D: foo as "any string goes here";
```

## Practical Stuff

A parser for the language is provided, as well as compilers for [graphviz]() and [mermaid](). The toolchain is implemented in Python, with no ambition of being particularly clever or efficient.

The parser has no separate lexing phase, as the language is very simple, and is written ad-hoc with no particular parsing architecture in mind.

## Formal Specification

TODO



