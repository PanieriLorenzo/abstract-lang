from dataclasses import dataclass


@dataclass
class StrRange:
    _ref: memoryview
    start: int
    end: int

    def __init__(self, s: bytes):
        self._ref = memoryview(s)
        self.start = 0
        self.end = len(self._ref)

    def __getitem__(self, key):
        if isinstance(key, slice):
            


a = "gneurhsk"
b = a[0:2]
print(id(a) - id(b))
