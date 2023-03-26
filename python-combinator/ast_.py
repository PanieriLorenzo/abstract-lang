from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional
from dataclasses import asdict
import json


@dataclass(eq=True, frozen=True)
class ASTNode:
    def dumps(self, indent: Optional[int] = None) -> str:
        return json.dumps(asdict(self), indent=indent)


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
        return Id(self.strs, namespace.strs + self.strs)

    @classmethod
    def empty(cls) -> Id:
        """An empty identifier is not valid, but it is useful as a base for
        constructing identifiers using addition"""
        return cls([])


@dataclass(eq=True, frozen=True)
class Map(ASTNode):
    ids: list[Id]

    def into_sets(self) -> list[NamedSet]:
        return [NamedSet.empty(i) for i in self.ids]


@dataclass(eq=True, frozen=True)
class SetBody(ASTNode):
    things_: list[Map | NamedSet]

    @classmethod
    def empty(cls) -> SetBody:
        return SetBody([])


@dataclass(eq=True, frozen=True)
class NamedSet(ASTNode):
    id_: Id
    set_: SetBody
    label: None | str

    @classmethod
    def new(cls, id_: Id, set_: None | SetBody, label: None | str) -> NamedSet:
        return cls(id_, SetBody.empty() if set_ is None else set_, label)

    @classmethod
    def empty(cls, id_: Id) -> NamedSet:
        return NamedSet.new(id_, None, None)


@dataclass(eq=True, frozen=True)
class Program(ASTNode):
    set_: SetBody


@dataclass
class TransformContext:
    """Base class to store the state during an AST transformation"""

    current_namespace: Id = Id.empty()

    def enter_namespace(self, namespace_id: Id):
        self.current_namespace += namespace_id

    def exit_namespace(self, num: int) -> list[tuple[Id, Id]]:
        return [self.current_namespace.pop() for _ in range(num)]
