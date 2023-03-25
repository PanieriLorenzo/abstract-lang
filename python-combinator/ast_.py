from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple


@dataclass(eq=True, frozen=True)
class ASTNode:
    pass


@dataclass(eq=True, frozen=True)
class Id(ASTNode):
    strs: list[str]
    absolute_strs: None | list[str] = None

    def __add__(self, other: Id) -> Id:
        """NOTE: this invalidates absolute_strs"""
        return Id(self.strs + other.strs)

    def __len__(self) -> int:
        return len(self.strs)

    def pop(self) -> Tuple[Id, Id]:
        """NOTE: this invalidates absolute_strs"""
        return Id([self.strs[-1]]), Id(self.strs[:-1])

    def make_absolute(self, namespace: Id) -> Id:
        """makes a relative Id absolute"""
        return Id(self.strs, self.strs + namespace.strs)


@dataclass(eq=True, frozen=True)
class Map(ASTNode):
    ids: list[Id]


@dataclass(eq=True, frozen=True)
class SetBody(ASTNode):
    things_: list[Map | NamedSet]


@dataclass(eq=True, frozen=True)
class NamedSet(ASTNode):
    id_: Id
    set_: SetBody
    label: None | str


@dataclass(eq=True, frozen=True)
class Program(ASTNode):
    set_: SetBody
