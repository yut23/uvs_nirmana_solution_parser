import enum


class ToolId(enum.Enum):
    VALVE = 1
    DEMUX = 2
    MUX = 3
    SENSE = 4
    BUFFER = 5
    INPUT = 6
    OUTPUT = 7
    PIPE = 8
    NEGATION = 9
    DELAY = 10
    MIXER = 11
    DEMUX_FLIPPED = 12
    MUX_FLIPPED = 13
    TOGGLE = 14
    RED = 15
    GREEN = 16
    CLEANER = 17
    TRANSLATE = 18
    YELLOW = 19


class MatrixPartId(enum.Enum):
    DRIVER = 0
    RELAY = 1
