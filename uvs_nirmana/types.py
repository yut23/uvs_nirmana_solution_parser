from __future__ import annotations

import abc
import dataclasses
import struct
from dataclasses import dataclass
from typing import BinaryIO, cast, overload

from typing_extensions import Self


def read_int(fp: BinaryIO) -> int:
    return cast(int, struct.unpack("<i", fp.read(4))[0])


def read_bool(fp: BinaryIO) -> bool:
    return fp.read(1)[0] != 0


class Parseable(abc.ABC):
    # pylint: disable=too-few-public-methods
    @classmethod
    @abc.abstractmethod
    def parse(cls, fp: BinaryIO) -> Self:
        raise NotImplementedError


@dataclass(frozen=True)
class Position(Parseable):
    column: int
    row: int

    def __add__(self, offset: Offset) -> Position:
        return Position(self.column + offset.cols, self.row + offset.rows)

    @overload
    def __sub__(self, other: Position) -> Offset:
        ...

    @overload
    def __sub__(self, other: Offset) -> Position:
        ...

    def __sub__(self, other: Position | Offset) -> Offset | Position:
        if isinstance(other, Position):
            return Offset(cols=self.column - other.column, rows=self.row - other.row)
        if isinstance(other, Offset):
            return Position(self.column - other.cols, self.row - other.rows)
        return NotImplemented

    def copy(self) -> Self:
        return dataclasses.replace(self)

    @classmethod
    def parse(cls, fp: BinaryIO) -> Self:
        column = read_int(fp)
        row = read_int(fp)
        return cls(column, row)


@dataclass(frozen=True)
class Offset(Parseable):
    cols: int
    rows: int

    def __add__(self, other: Offset) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(self.cols + other.cols, self.rows + other.rows)

    def __sub__(self, other: Offset) -> Offset:
        if not isinstance(other, Offset):
            return NotImplemented
        return Offset(self.cols - other.cols, self.rows - other.rows)

    def copy(self) -> Self:
        return dataclasses.replace(self)

    @classmethod
    def parse(cls, fp: BinaryIO) -> Self:
        cols = read_int(fp)
        rows = read_int(fp)
        return cls(cols, rows)


@dataclass
class BoundingBox:
    """low is the lower-left corner, high is 1 past the upper-right corner."""

    low: Position
    high: Position

    @property
    def size(self) -> Offset:
        return self.high - self.low

    def update(self, other: BoundingBox | Position) -> Self:
        """Updates this BoundingBox to include `other`."""
        if isinstance(other, Position):
            other = BoundingBox(other, other + Offset(1, 1))
        self.low = Position(
            column=min(self.low.column, other.low.column),
            row=min(self.low.row, other.low.row),
        )
        self.high = Position(
            column=max(self.high.column, other.high.column),
            row=max(self.high.row, other.high.row),
        )
        assert other in self
        return self

    def __contains__(self, arg: Position | BoundingBox) -> bool:
        """Return True if arg is entirely within this bounding box."""
        if isinstance(arg, Position):
            return (
                self.low.column <= arg.column < self.high.column
                and self.low.row <= arg.row < self.high.row
            )
        if isinstance(arg, BoundingBox):
            return (
                self.low.column <= arg.low.column
                and arg.high.column <= self.high.column
                and self.low.row <= arg.low.row
                and arg.high.row <= self.high.row
            )
        msg = f"invalid type passed to BoundingBox.__contains__: {type(arg)}"
        raise TypeError(msg)

    def copy(self) -> Self:
        return dataclasses.replace(self)
