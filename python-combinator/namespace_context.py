from __future__ import annotations
from ast_ import Id, Optional


class NamespaceContext:
    """Base class to store the state during an AST transformation"""

    current_namespace: Id = Id.empty()

    @classmethod
    def empty(cls) -> NamespaceContext:
        return cls(Id.empty())

    def __init__(
        self, namespace_tip: Id, namespace_base: Optional[NamespaceContext] = None
    ):
        if namespace_base:
            self.current_namespace = namespace_base.current_namespace + namespace_tip
            self.length_stack = namespace_base.length_stack + [len(namespace_tip)]
        else:
            self.current_namespace = namespace_tip
            self.length_stack = [len(namespace_tip)]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        tip_length = self.length_stack.pop()
        for _ in range(tip_length):
            self.current_namespace.pop()
