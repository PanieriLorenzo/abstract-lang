from parser_ import parse
from ast_ import ASTNode
from preprocessor import preprocess
from optimizer import optimize
import codegen_aml


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

s3 = """\
A.A;
A.A;
"""

s4 = """\
A {
    B;
    C;
    B -> C;
}
"""

s5 = """\
A {
    B;
    C;
    D;
    B -> C -> D;
}
"""

if __name__ == "__main__":
    print(codegen_aml.codegen(optimize(parse(preprocess(s1)))))
