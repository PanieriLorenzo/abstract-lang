from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TraitPPrint:
    """a trait that allows pretty printing. You just have to implement _pprint()"""

    def pprint(self):
        """implemented for you"""
        self._pprint(0)

    def _pprint(self, indent: int):
        """must be implemented"""
        raise NotImplementedError


@dataclass
class Id(TraitPPrint):
    """minimum cardinality 1, e.g. `A`"""

    left: str
    right: None | Id

    @classmethod
    def flat(cls, s: str) -> Id:
        return cls(s, None)

    def _pprint(self, indent: int):
        print("   " * indent, "id")
        print("   " * (indent + 1), self.left)
        if self.right:
            self.right._pprint(indent + 1)

    def _get_ancestry(self, l: list[Id]) -> list[Id]:
        

    def get_ancestry(self) -> list[Id]:
        """get a list of every ancestor Id recursively

        ## Examples
        - `A.B.C` becomes `[A, B, C]`
        """



@dataclass
class Map(TraitPPrint):
    """minumum cardinality 2, e.g. `A->B`"""

    left: Id
    right: Id | Map

    def _pprint(self, indent: int):
        print("   " * indent, "map")
        self.left._pprint(indent + 1)
        self.right._pprint(indent + 1)


@dataclass
class SetBody(TraitPPrint):
    """minimum cardinality 0, e.g. `A{}`"""

    left: None | Thing
    right: None | SetBody

    @classmethod
    def empty(cls) -> SetBody:
        return cls(None, None)

    @classmethod
    def one(cls, t: Thing) -> SetBody:
        return cls(t, None)

    def _pprint(self, indent: int):
        if not self.left:
            return
        self.left._pprint(indent)
        if not self.right:
            return
        self.right._pprint(indent)


@dataclass
class NamedSet(TraitPPrint):
    id: Id
    set_: SetBody

    @classmethod
    def empty(cls, i: str | Id) -> NamedSet:
        if type(i) == str:
            return cls(Id.flat(i), SetBody.empty())
        if type(i) == Id:
            return cls(i, SetBody.empty())
        raise TypeError

    def _pprint(self, indent: int):
        print("   " * indent, "named_set")
        self.id._pprint(indent + 1)
        self.set_._pprint(indent + 1)


ASTNode = NamedSet | SetBody | Map | Id | None


Thing = NamedSet | Map
