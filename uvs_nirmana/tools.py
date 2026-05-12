from __future__ import annotations

from dataclasses import dataclass

from .enums import ToolId
from .types import Offset


@dataclass(frozen=True, kw_only=True)
class PortProperties:
    is_output: bool
    offset: Offset


@dataclass(frozen=True, kw_only=True)
class ToolType:
    id: ToolId
    size: Offset
    only_one: bool = False
    ports: tuple[PortProperties, ...]


def parse_ports(
    inputs: list[tuple[int, int]], outputs: list[tuple[int, int]]
) -> tuple[PortProperties, ...]:
    ports = []
    for offset in inputs:
        ports.append(PortProperties(is_output=False, offset=Offset(*offset)))
    for offset in outputs:
        ports.append(PortProperties(is_output=True, offset=Offset(*offset)))
    return tuple(ports)


_tools = [
    ToolType(id=ToolId.PIPE, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(id=ToolId.SENSE, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(id=ToolId.VALVE, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(
        id=ToolId.DEMUX,
        size=Offset(1, 2),
        ports=parse_ports([(0, 1)], [(0, 0), (0, 1)]),
    ),
    ToolType(
        id=ToolId.MUX, size=Offset(1, 2), ports=parse_ports([(0, 0), (0, 1)], [(0, 1)])
    ),
    ToolType(
        id=ToolId.DEMUX_FLIPPED,
        size=Offset(1, 2),
        ports=parse_ports([(0, 0)], [(0, 0), (0, 1)]),
    ),
    ToolType(
        id=ToolId.MUX_FLIPPED,
        size=Offset(1, 2),
        ports=parse_ports([(0, 0), (0, 1)], [(0, 0)]),
    ),
    ToolType(
        id=ToolId.BUFFER, size=Offset(2, 3), ports=parse_ports([(0, 1)], [(1, 1)])
    ),
    ToolType(
        id=ToolId.NEGATION,
        size=Offset(2, 3),
        ports=parse_ports([(0, 1)], [(1, 1)]),
        only_one=True,
    ),
    ToolType(id=ToolId.DELAY, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(
        id=ToolId.MIXER,
        size=Offset(2, 3),
        ports=parse_ports([(0, 0), (0, 2)], [(1, 1)]),
        only_one=True,
    ),
    ToolType(
        id=ToolId.TOGGLE,
        size=Offset(1, 3),
        ports=parse_ports([(0, 0), (0, 2)], [(0, 1)]),
    ),
    ToolType(
        id=ToolId.CLEANER, size=Offset(2, 3), ports=parse_ports([(0, 1)], [(1, 1)])
    ),
    ToolType(id=ToolId.GREEN, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(id=ToolId.RED, size=Offset(1, 1), ports=parse_ports([(0, 0)], [(0, 0)])),
    ToolType(
        id=ToolId.TRANSLATE,
        size=Offset(2, 3),
        ports=parse_ports([(0, 1)], [(1, 1)]),
        only_one=True,
    ),
    ToolType(id=ToolId.INPUT, size=Offset(1, 1), ports=parse_ports([], [(0, 0)])),
    ToolType(id=ToolId.OUTPUT, size=Offset(1, 1), ports=parse_ports([(0, 0)], [])),
]
TOOLS = {tool.id: tool for tool in _tools}
