from __future__ import annotations
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class ASTNode:
    pass


@dataclass(eq=True, frozen=True)
class Id(ASTNode):
    strs: list[str]


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
