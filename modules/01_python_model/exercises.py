"""Module 01 reference implementations for the Python data model."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class MutableDemo:
    """Illustrates mutable vs immutable built-ins."""

    items: list[int]

    def append(self, value: int) -> None:
        self.items.append(value)


@dataclass(frozen=True)
class Vector2:
    """Immutable value object with dunder protocol."""

    x: float
    y: float

    def __repr__(self) -> str:
        return f"Vector2(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class MiniSequence:
    """Minimal sequence protocol over a backing list."""

    def __init__(self, values: list[int]) -> None:
        self._values = list(values)

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, index: int) -> int:
        return self._values[index]

    def __iter__(self) -> Iterator[int]:
        return iter(self._values)
