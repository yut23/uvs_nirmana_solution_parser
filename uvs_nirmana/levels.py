from dataclasses import dataclass, field

from .enums import ToolId
from .types import BoundingBox, Position

_DEFAULT_TOOLS = frozenset(
    {
        ToolId.PIPE,
        ToolId.SENSE,
        ToolId.VALVE,
        ToolId.MUX,
        ToolId.MUX_FLIPPED,
        ToolId.DEMUX,
        ToolId.DEMUX_FLIPPED,
    }
)


@dataclass(frozen=True, kw_only=True, order=True)
class Level:
    id: int = field(compare=False)
    order: int
    title: str
    subtitle: str
    first_solution_number: int = 1
    allowed_tools: frozenset[ToolId]
    allow_matrix: bool = True

    @property
    def prefix(self) -> str:
        return self.title.lower().replace("-", "").replace(" ", "-")

    def __str__(self) -> str:
        if self.title == "Unknown":
            return f"{self.title} ({self.subtitle})"
        return self.title


_levels = [
    Level(
        id=26,
        order=1,
        title="Komidai-2",
        subtitle="Holographic Civilization",
        allowed_tools=frozenset({ToolId.PIPE}),
        allow_matrix=False,
    ),
    Level(
        id=9,
        order=2,
        title="B7 Mimohe",
        subtitle="Abandoned Transfer Station",
        allowed_tools=frozenset({ToolId.PIPE, ToolId.SENSE, ToolId.VALVE}),
        allow_matrix=False,
    ),
    Level(
        id=21,
        order=3,
        title="Hrum-Simigan",
        subtitle="Hrum-Simigan",
        allowed_tools=frozenset(
            (_DEFAULT_TOOLS - {ToolId.DEMUX, ToolId.DEMUX_FLIPPED}) | {ToolId.TRANSLATE}
        ),
    ),
    Level(
        id=25,
        order=4,
        title="Nagarahara",
        subtitle="The Nebula of Re-Observation",
        allowed_tools=frozenset(
            (_DEFAULT_TOOLS - {ToolId.DEMUX, ToolId.DEMUX_FLIPPED})
            | {ToolId.RED, ToolId.GREEN}
        ),
    ),
    Level(
        id=1,
        order=5,
        title="J9 Takka",
        subtitle="Infected Transfer Station",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.MIXER}),
    ),
    Level(
        id=8,
        order=6,
        title="Atali-4",
        subtitle="Alien Mining Colony",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.TOGGLE}),
    ),
    Level(
        id=14,
        order=7,
        title="Syghinan Prime",
        subtitle="Graveyard of the Syghinan Empire",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.GREEN, ToolId.CLEANER}),
    ),
    Level(
        id=13,
        order=8,
        title="D7 Balura",
        subtitle="Phase-Shifted Transfer Station",
        allowed_tools=_DEFAULT_TOOLS,
    ),
    Level(
        id=22,
        order=9,
        title="Object Jaguda",
        subtitle="Space-Time Anomaly",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.TOGGLE}),
    ),
    Level(
        id=11,
        order=10,
        title="Udyana-3",
        subtitle="Home of the Eternal Society",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.BUFFER}),
    ),
    Level(
        id=24,
        order=11,
        title="N.S. Huoh",
        subtitle="Compromised Generation Ship",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.RED, ToolId.NEGATION}),
    ),
    Level(
        id=2,
        order=12,
        title="Kita Oriens",
        subtitle="Nonrepeating Crystal Field",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.DELAY}),
    ),
    Level(
        id=12,
        order=13,
        title="Wakhsh Prime",
        subtitle="Hostile Alien Homeworld",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.TOGGLE, ToolId.BUFFER}),
    ),
    Level(
        id=17,
        order=14,
        title="Mathura Nova",
        subtitle="Home of the Great Council",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.RED, ToolId.NEGATION}),
    ),
    Level(
        id=5,
        order=15,
        title="Maha Talakan",
        subtitle="Cultural Exchange Nexus",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.DELAY}),
    ),
    Level(
        id=3,
        order=16,
        title="Nalanda-1",
        subtitle="The Library Planet",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.BUFFER}),
    ),
    Level(
        id=15,
        order=17,
        title="The Batira Object",
        subtitle="Galactic Barrier",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.TOGGLE}),
    ),
    Level(
        id=7,
        order=18,
        title="Kamarupa",
        subtitle="The Dream-Reality Realm",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.BUFFER}),
    ),
    Level(
        id=4,
        order=19,
        title="U.V.S. Nayuta",
        subtitle="Sister Ship of the U.V.S. Nirmana",
        allowed_tools=_DEFAULT_TOOLS,
    ),
    Level(
        id=16,
        order=20,
        title="Invakan-3",
        subtitle="Endangered Civilization",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.DELAY}),
    ),
    Level(
        id=19,
        order=21,
        title="K.N. Uda",
        subtitle="Gateway to Tenfold Void",
        allowed_tools=_DEFAULT_TOOLS,
    ),
    Level(
        id=18,
        order=22,
        title="SMO",
        subtitle="Spherical Metabolic Object",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.TOGGLE}),
    ),
    Level(
        id=10,
        order=23,
        title="Gostana-1",
        subtitle="Ruins of a Lost Civilization",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.RED, ToolId.DELAY}),
    ),
    Level(
        id=20,
        order=24,
        title="N2 Kurana",
        subtitle="Devout Transfer Station",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.GREEN, ToolId.BUFFER}),
    ),
    Level(
        id=6,
        order=25,
        title="Tamra Occidens",
        subtitle="Negated Civilization",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.NEGATION}),
    ),
    Level(
        id=23,
        order=26,
        title="S1 Varnu",
        subtitle="Distant Transfer Station",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.GREEN, ToolId.RED}),
    ),
    Level(
        id=27,
        order=27,
        title="Z0 Yani",
        subtitle="Final Transfer Station",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.BUFFER}),
    ),
    Level(
        id=28,
        order=28,
        title="Unknown",
        subtitle="The Edge of the Universe",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.DELAY, ToolId.BUFFER}),
    ),
    Level(
        id=29,
        order=29,
        title="Unknown",
        subtitle="Gateway to Nirodha",
        first_solution_number=4,
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.NEGATION}),
    ),
    Level(
        id=30,
        order=30,
        title="Nirodha",
        subtitle="The End of the Universe",
        allowed_tools=_DEFAULT_TOOLS | frozenset({ToolId.DELAY, ToolId.BUFFER}),
    ),
]
LEVELS = {level.id: level for level in _levels}


LEVEL_BBOX = BoundingBox(low=Position(1, 0), high=Position(13, 11))
