from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Id:
    parent: None | Id
    s: str


@dataclass
class Source:
    s: str


@dataclass
class Map:
    left: Id
    right: Id | Map | Source


@dataclass
class SetBody:
    elements: list[ASTNode]


@dataclass
class NamedSet:
    id: Id
    set_: SetBody


ASTNode \
    = NamedSet \
    | SetBody \
    | Map \
    | Id \
    | None