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
