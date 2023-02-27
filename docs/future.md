# Future

## Make the language regular

Set members should be strictly delimited by semicolons:

```
# this will be wrong
A {
	A;
	B {}	# missing semicolon
	C;
}			# missing semicolon

# this is the new syntax
A {
	A;
	B {};
	C;
};
```
