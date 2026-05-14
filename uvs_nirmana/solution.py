from __future__ import annotations

import os
from dataclasses import dataclass
from typing import BinaryIO

from typing_extensions import Self

from .enums import MatrixPartId, ToolId
from .levels import LEVEL_BBOX, LEVELS, Level
from .tools import TOOLS, ToolType
from .types import (
    BoundingBox,
    Offset,
    Parseable,
    Position,
    read_bool,
    read_int,
)


@dataclass(frozen=True, kw_only=True)
class Metrics:
    width: int
    height: int
    flux: int

    def __str__(self) -> str:
        return f"{self.width}/{self.height}/{self.flux}"


class InvalidMetricError(Exception):
    pass


class InvalidSolutionError(Exception):
    pass


@dataclass(frozen=True, kw_only=True)
class Solution(Parseable):
    # pylint: disable=too-many-instance-attributes
    version: int
    level_id: int
    solved: bool
    width: int
    height: int
    flux: int

    pipeline_parts: tuple[Part, ...]
    matrix_parts: tuple[MatrixPart, ...]

    @classmethod
    def parse(cls, fp: BinaryIO) -> Self:
        version = read_int(fp)
        if version != 1:
            msg = f"Unrecognized solution file version: {version}"
            raise ValueError(msg)
        level_id = read_int(fp)
        _unknown = read_int(fp)
        solved = read_bool(fp)
        width = read_int(fp)
        height = read_int(fp)
        flux = read_int(fp)

        num_pipeline_parts = read_int(fp)
        pipeline_parts = tuple(Part.parse(fp) for _ in range(num_pipeline_parts))

        num_matrix_parts = read_int(fp)
        matrix_parts = tuple(MatrixPart.parse(fp) for _ in range(num_matrix_parts))

        return cls(
            version=version,
            level_id=level_id,
            solved=solved,
            width=width,
            height=height,
            flux=flux,
            pipeline_parts=pipeline_parts,
            matrix_parts=matrix_parts,
        )

    @classmethod
    def read(cls, path: os.PathLike[str]) -> Self:
        with open(path, "rb") as f:
            return cls.parse(f)

    @property
    def level(self) -> Level | None:
        return LEVELS.get(self.level_id, None)

    def check_all(self) -> None:
        level = self.level
        # check matrix parts
        if level is not None and not level.allow_matrix and self.matrix_parts:
            msg = f"Matrix parts not allowed in {level}"
            raise InvalidSolutionError(msg)
        # check allowed tools
        if level is not None:
            allowed_tools = level.allowed_tools | {ToolId.INPUT, ToolId.OUTPUT}
            for part in self.pipeline_parts:
                if part.tool_id not in allowed_tools:
                    msg = f"Tool not allowed in {level}: {part.tool}"
                    raise InvalidSolutionError(msg)
        # TODO: check for overlap
        tool_bbox = self.calc_bbox()
        self.check_pipes()
        self.check_metrics(tool_bbox)

    def calc_bbox(self) -> BoundingBox | None:
        # check level bounding box
        tool_bbox: BoundingBox | None = None
        for i, part in enumerate(self.pipeline_parts):
            if part.tool_id in {ToolId.INPUT, ToolId.OUTPUT}:
                continue
            if tool_bbox is None:
                tool_bbox = part.tool_bbox()
            else:
                tool_bbox.update(part.tool_bbox())
            if tool_bbox not in LEVEL_BBOX:
                msg = f"{part.tool_id.name.title()} at index {i} is outside level bounding box: {part}"
                raise InvalidSolutionError(msg)
            if part.pipe_bbox() not in LEVEL_BBOX:
                msg = f"Pipes for part at index {i} are outside level bounding box: {part}"
                raise InvalidSolutionError(msg)
        return tool_bbox

    def check_pipes(self) -> None:
        for part in self.pipeline_parts:
            for i, (offset, port) in enumerate(zip(part.pipe_offsets, part.tool.ports)):
                desc = f"Pipe {i} of {part.tool_id.name.title()} at {part.pos}"
                if port.is_output:
                    if abs(offset.rows) > min(abs(offset.cols), 2):
                        msg = f"{desc} is too long vertically ({offset})"
                        raise InvalidSolutionError(msg)
                    if offset.cols < 0:
                        msg = f"{desc} goes backward ({offset})"
                        raise InvalidSolutionError(msg)
                else:
                    # input pipe must be (0, 0)
                    if offset.cols != 0 or offset.rows != 0:
                        msg = f"{desc} is an input and has a non-zero offset ({offset})"
                        raise InvalidSolutionError(msg)

    def check_metrics(self, tool_bbox: BoundingBox | None = None) -> None:
        if tool_bbox is None:
            tool_bbox = self.calc_bbox()
        # check width and height
        metrics = self.get_metrics()
        if metrics is None:
            return
        if tool_bbox is None:
            width = 0
            height = 0
        else:
            width = tool_bbox.size.cols
            height = tool_bbox.size.rows
        if width != metrics.width:
            msg = f"Width doesn't match: calculated {width}, read {metrics.width}"
            raise InvalidMetricError(msg)
        if height != metrics.height:
            msg = f"Height doesn't match: calculated {height}, read {metrics.height}"
            raise InvalidMetricError(msg)
        # check flux
        flux = len(self.matrix_parts)
        if flux != metrics.flux:
            msg = f"Flux doesn't match: calculated {flux}, read {metrics.flux}"
            raise InvalidMetricError(msg)

    def get_metrics(self) -> Metrics | None:
        if not self.solved or 0x7FFFFFFF in {self.width, self.height, self.flux}:
            return None
        return Metrics(width=self.width, height=self.height, flux=self.flux - 1)


@dataclass(kw_only=True)
class Part(Parseable):
    tool_id: ToolId
    pos: Position
    pipe_offsets: list[Offset]

    @property
    def tool(self) -> ToolType:
        return TOOLS[self.tool_id]

    def tool_bbox(self) -> BoundingBox:
        """Bounding box of just this tool (used to calculate width and height)."""
        return BoundingBox(
            low=self.pos,
            high=self.pos + self.tool.size,
        )

    def pipe_bbox(self) -> BoundingBox:
        """Bounding box of this tool plus all outgoing pipes."""
        bbox = self.tool_bbox().copy()
        for pipe_offset, port in zip(self.pipe_offsets, self.tool.ports):
            bbox.update(self.pos + pipe_offset + port.offset)
        return bbox

    @classmethod
    def parse(cls, fp: BinaryIO) -> Part:
        tool_id = ToolId(read_int(fp))
        pos = Position.parse(fp)
        num_pipes = read_int(fp)
        pipe_offsets = [Offset.parse(fp) for _ in range(num_pipes)]
        return cls(tool_id=tool_id, pos=pos, pipe_offsets=pipe_offsets)


@dataclass(kw_only=True)
class MatrixPart(Parseable):
    pos: Position
    type: MatrixPartId

    @classmethod
    def parse(cls, fp: BinaryIO) -> Self:
        pos = Position.parse(fp)
        type_ = MatrixPartId(read_int(fp))
        return cls(pos=pos, type=type_)
