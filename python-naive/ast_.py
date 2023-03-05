from __future__ import annotations
from dataclasses import dataclass
from itertools import chain


@dataclass(eq=True, frozen=True)
class TraitPPrint:
    """a trait that allows pretty printing. You just have to implement _pprint()"""

    def pprint(self):
        """implemented for you"""
        self._pprint(0)

    def _pprint(self, indent: int):
        """must be implemented"""
        raise NotImplementedError


@dataclass(eq=True, frozen=True)
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

    def head(self) -> tuple[Id, Id | None]:
        return Id.flat(self.left), self.right

    def is_flat(self) -> bool:
        return self.right is None

    def remove(self) -> None | Id:
        if self.right is None:
            return None
        return Id(self.left, self.right.remove())

    @classmethod
    def from_list(cls, l: list[str]) -> Id:  # noqa E741
        if len(l) == 0:
            raise SystemError
        if len(l) == 1:
            return Id.flat(l[0])
        return Id(l[0], Id.from_list(l[1:]))

    def __iter__(self):
        cur = self
        while True:
            if cur is None:
                return
            yield cur.left
            cur = cur.right

    def __add__(self, other: Id) -> Id:
        """join two Ids

        ## Examples
        - `A + B` becomes `A.B`
        - `A.B + C.D` becomes `A.B.C.D`
        """
        lhs = list(self)
        rhs = list(other)
        return Id.from_list(lhs + rhs)

    def __radd__(self, other: None) -> Id:
        return self

    def _percolate(self, parent: Id) -> Id:
        return parent + self


@dataclass(eq=True, frozen=True)
class Map(TraitPPrint):
    """minumum cardinality 2, e.g. `A->B`"""

    left: Id
    right: Id | Map

    def _pprint(self, indent: int):
        print("   " * indent, "map")
        self.left._pprint(indent + 1)
        self.right._pprint(indent + 1)

    def _percolate(self, parent: Id) -> Map:
        """Pull this map out of the parent"""
        return Map(parent + self.left, self.right._percolate(parent))

    def __iter__(self):
        cur = self
        while True:
            if type(cur) == Id:
                yield cur
                break
            yield cur.left
            cur = cur.right
    
    def extract_sets(self) -> list[NamedSet]:
        ret = [NamedSet.empty(self.left).normalize()]
        if type(self.right) == Id:
            return ret + [NamedSet.empty(self.right).normalize()]
        return ret + self.right.extract_sets()  # type: ignore

    def expand(self) -> list[Map]:
        flat = list(self)
        if len(flat) == 2:
            return [self]
        return [Map(e, flat[i + 1]) for i, e in enumerate(flat[:-1])]


@dataclass(eq=True, frozen=True)
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

    def normalize(self) -> SetBody:
        if self.left is None:
            return self
        
        ret = SetBody(
            self.left.normalize() if type(self.left) == NamedSet else self.left,
            self.right.normalize() if self.right is not None else None,
        )
        if type(self.left) == Map:
            for s in self.left.extract_sets():
                ret = ret.insert(s)
        return ret



    def insert(self, other: NamedSet | Map) -> SetBody:
        return SetBody(other, self)

    def __iter__(self):
        cur = self
        while True:
            if cur is None or cur.left is None:
                return
            yield cur.left
            cur = cur.right

    def is_empty(self) -> bool:
        if self.left is None and self.right is not None:
            raise SystemError
        return self.left is None

    @classmethod
    def from_list(cls, l: list[Thing]) -> SetBody:  # noqa E741
        if len(l) == 0:
            return SetBody.empty()
        return SetBody(l[0], SetBody.from_list(l[1:]))

    def dedupe(self) -> SetBody:
        return SetBody.from_list(list(set(self)))


@dataclass(eq=True, frozen=True)
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

    def is_empty(self) -> bool:
        return self.set_.is_empty()

    def _pprint(self, indent: int):
        print("   " * indent, "named_set")
        self.id._pprint(indent + 1)
        self.set_._pprint(indent + 1)

    def normalize(self) -> NamedSet:
        hd, tail = self.id.head()
        if tail is None:
            return NamedSet(self.id, self.set_.normalize())
        return NamedSet(
            hd, self.set_.insert(NamedSet.empty(tail).normalize()).normalize()
        )

    def __iter__(self):
        return iter(self.set_)

    def dedupe(self) -> NamedSet:
        return NamedSet(self.id, self.set_.dedupe())

    def to_list(self) -> list[Thing]:
        return list(self.set_)

    def _percolate(
        self, parent: None | Id, top_level: bool = False
    ) -> tuple[NamedSet, list[Map]]:
        new_parent = parent + self.id if not top_level else None

        sets: list[NamedSet] = [s for s in self if type(s) == NamedSet]
        maps: list[Map] = [m for m in self if type(m) == Map]

        # if we are on the first layer, parent is None and we don't need to
        # percolate maps, as it should have no effect
        if not top_level:
            maps = [m._percolate(new_parent) for m in maps]  # type: ignore

        aux = [s._percolate(new_parent) for s in sets]
        sets2: list[Thing] = [p[0] for p in aux]
        maps += chain(*[p[1] for p in aux])

        if top_level:
            return NamedSet(self.id, SetBody.from_list(sets2 + list(maps))), maps
        return NamedSet(self.id, SetBody.from_list(sets2)), maps

    def percolate(self) -> NamedSet:
        p = self._percolate(None, True)
        return p[0]

    def expand(self) -> NamedSet:
        sets: list[NamedSet] = [s.expand() for s in self if type(s) == NamedSet]
        maps: list[Map] = list(chain(*[m.expand() for m in self if type(m) == Map]))  # type: ignore # noqa E501
        return NamedSet(self.id, SetBody.from_list(sets + maps))


ASTNode = NamedSet | SetBody | Map | Id | None


Thing = NamedSet | Map
