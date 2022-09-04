from abc import ABC
from dataclasses import dataclass


class MirageState(ABC):
    Off = None
    Default = None


@dataclass
class MirageStateOn(MirageState):
    red_freq: int
    green_freq: int
    blue_freq: int


class MirageStateOff(MirageState):
    pass


MirageState.Off = MirageStateOff()
MirageState.Default = MirageStateOn(330, 330, 330)
