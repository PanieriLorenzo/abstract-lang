from parser import *
from ast_ import *
from preprocessor import *

s = \
"""# this is a comment lmao
A;
B {}
U -> V;
D -> C.A;
C.B -> D;
Foo -> Bar -> Baz.A;
Baz.B -> Foo.A;
C {
    A;
    B {}
    C { A; }
    D -> C.A;
}
Foo {
    C;
}

# some fucky shit:
X    . Y.Z ->Z.     Y.   X ;
;; ;    ;; ;   ;   ;;; ;
"""

if __name__ == "__main__":
    
    print(parse_source(preprocess(s)))