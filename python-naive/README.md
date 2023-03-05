# Python Naive

This implementation is naive, in the sense that it doesn't try to be extensible or particularly efficient, it just tries to be as simple and straight forward as possible.
It's not naive in the sense that it's of poor quality.

It's almost entirely functional, classes are only used as immutable dataclasses. No attempt is made to make interfaces such as visitors and such, for the sake of simplicity.
Every compiler pass is just a recursive function that pattern matches the head of its input and calls itself recursively on the remainder of the input. Very basic, veryntextbook functional programming.

It doesn't use lists a lot, instead it uses recursive types. Maybe in hindsight it would have been better to just use lists, but then again, it's nice to have a refernce implementation that is purely algebraic.


## Passes

### Parser

### Optimizer

Examples:

```python
# before
A;
B;

# after (no change)
A;
B;
```

```python
# before
A {
    A;
}
A {
    B;
}

# after
A {
    A;
    B;
}
```

```python
# before
A.A;
A.B;

# after
A {
    A;
    B;
}
```


```python
#before
A.A;

#after
A {
    A {}
}
```