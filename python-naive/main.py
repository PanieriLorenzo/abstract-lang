from parser_ import *
from ast_ import *
from preprocessor import *
from ast_viz import *
from optimizer import *


s1 = """# this is a comment lmao
A;
B {}
U -> V;
D -> C.A;
C.B -> D;
Foo -> Bar -> Baz.A;
A.A.A.A -> B.B.B.B -> C.C.C.C;
A .A. A . A -> B   .B  .    B. B    ->C. C.  C.   C        ;;; ;;
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
;; ;    ;; ;  ;;;
"""

s2 = """\
A.A;
B.B;
"""

if __name__ == "__main__":

    a = parse(preprocess(s1))
    a.pprint()
    a.normalize().pprint()
