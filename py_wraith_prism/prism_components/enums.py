from enum import IntEnum


class ColorSupport(IntEnum):
    None_ = 0,
    Specific = 1,
    All = 2


class Speed(IntEnum):
    Slowest = 0,
    Slow = 1,
    Medium = 2,
    Fast = 3,
    Fastest = 4


class Brightness(IntEnum):
    Low = 0,
    Medium = 1,
    High = 2


class RotationDirection(IntEnum):
    Clockwise = 0,
    CounterClockwise = 1
