from typing import NamedTuple, Mapping
from py_wraith_prism.prism_components.enums import ColorSupport, Brightness, Speed
from enum import Enum


class _PrismMode:
    '''
    Python NamedTuple doesn't allow for proper subclassing.
    Subclasses of this should contain the following fields (see notes):

    brightnesses: Mapping[Brightness, int]
    colorSupport: ColorSupport
    '''

    def find_brightness(self, value, default=None):
        # noinspection PyUnresolvedReferences
        for (b, bv) in self.brightnesses.items():
            if bv == value:
                return b
        return default

    def find_speed(self, value, default=None):
        # noinspection PyUnresolvedReferences
        for (s, sv) in self.speeds.items():
            if sv == value:
                return s
        return default


def map_brightness(low, medium, high):
    return {
        Brightness.Low: low,
        Brightness.Medium: medium,
        Brightness.High: high
    }


def map_speed(slowest, slow, medium, fast, fastest):
    return {
        Speed.Slowest: slowest,
        Speed.Slow: slow,
        Speed.Medium: medium,
        Speed.Fast: fast,
        Speed.Fastest: fastest
    }


class _BasicPrismMode(NamedTuple):
    mode: int
    speeds: Mapping[Speed, int] = {}
    brightnesses: Mapping[Brightness, int] = map_brightness(0x4C, 0x99, 0xFF)
    color_support: ColorSupport = ColorSupport.None_


class BasicPrismMode(_BasicPrismMode, _PrismMode, Enum):
    Off = _BasicPrismMode(0, brightnesses={})
    Static = _BasicPrismMode(1, color_support=ColorSupport.Specific)
    Cycle = _BasicPrismMode(2, map_speed(0x96, 0x8C, 0x80, 0x6E, 0x68), map_brightness(0x10, 0x40, 0x7F)),
    Breathe = _BasicPrismMode(3, map_speed(0x3C, 0x37, 0x31, 0x2C, 0x26), color_support=ColorSupport.All)

    @classmethod
    def from_mode(cls, mode: int):
        return next((m for m in cls if m.mode == mode))


class _PrismRingMode(NamedTuple):
    channel: int
    mode: int
    speeds: Mapping[Speed, int] = {}
    color_support: ColorSupport = ColorSupport.None_
    brightnesses: Mapping[Brightness, int] = map_brightness(0x4C, 0x99, 0xFF)
    supports_direction: bool = False
    color_source: int = 0x20


class PrismRingMode(_PrismRingMode, _PrismMode, Enum):
    Off = _PrismRingMode(
        0xFE, 0, brightnesses={})
    Static = _PrismRingMode(
        0, 0xFF, color_support=ColorSupport.Specific)
    Breathe = _PrismRingMode(
        1, 0xFF, map_speed(0x3C, 0x37, 0x31, 0x2C, 0x26), ColorSupport.All)
    Cycle = _PrismRingMode(
        2, 0xFF, map_speed(0x96, 0x8C, 0x80, 0x6E, 0x68),
        brightnesses=map_brightness(0x10, 0x40, 0x7F))
    Rainbow = _PrismRingMode(
        7, 5, map_speed(0x72, 0x68, 0x64, 0x62, 0x61), color_source=0)
    Bounce = _PrismRingMode(
        8, 0xFF, map_speed(0x77, 0x74, 0x6E, 0x6B, 0x67), color_source=0x80)
    Chase = _PrismRingMode(
        9, 0xC3, map_speed(0x77, 0x74, 0x6E, 0x6B, 0x67), ColorSupport.All, supports_direction=True)
    Swirl = _PrismRingMode(
        0xA, 0x4A, map_speed(0x77, 0x74, 0x6E, 0x6B, 0x67), ColorSupport.All, supports_direction=True)
    Morse = _PrismRingMode(
        0xB, 5, color_support=ColorSupport.All, brightnesses={}, color_source=0)

    @classmethod
    def from_mode(cls, mode: int):
        return next((m for m in cls if m.mode == mode))
