import itertools
from abc import ABC, abstractmethod
from typing import List, Sequence, Iterable

from colour import Color

from py_wraith_prism.channel_values import ChannelValues
from py_wraith_prism.morse import morse_or_text_to_bytes, bytes_to_morse_or_text
from py_wraith_prism.prism_components.enums import Speed, Brightness, ColorSupport, \
    RotationDirection
from py_wraith_prism.prism_components.mirage_state import MirageState
from py_wraith_prism.prism_components.prism_mode import BasicPrismMode, PrismRingMode
from py_wraith_prism.usb.hid_device_manager import UsbInterface


class PrismComponent(ABC):
    def __init__(self, usb: UsbInterface, mode: BasicPrismMode or PrismRingMode):
        self._usb: UsbInterface = usb

        self.mode: BasicPrismMode or PrismRingMode = mode
        self.color: Color = Color("black")
        self.speed: Speed = Speed.Medium
        self.brightness: Brightness = Brightness.Medium

        self.use_random_color: bool = False
        self._saved_byte_values: Sequence[int] = []

    @property
    @abstractmethod
    def channel(self):
        pass

    def save(self):
        self._saved_byte_values = self._byte_values

    @property
    def _color_bytes(self) -> List[int]:
        return [int(self.color.red * 255),
                int(self.color.green * 255),
                int(self.color.blue * 255)]

    @property
    def has_unsaved_changes(self) -> bool:
        values = self._byte_values
        saved_values = self._saved_byte_values
        if len(values) != len(saved_values):
            return True

        for value, savedValue in zip(values, saved_values):
            if value != savedValue:
                return True
        return False

    @property
    @abstractmethod
    def _byte_values(self) -> Sequence[int]:
        pass

    @abstractmethod
    def _reload_values(self):
        pass

    def submit_values(self):
        data = itertools.chain([0x51, 0x2C, 1, 0], self._byte_values, [0, 0, 0])
        self._usb.send_bytes(data, filler=0xFF)

    def _fetch_channel_values(self) -> ChannelValues:
        return ChannelValues(self._usb.send_bytes([0x52, 0x2C, 1, 0, self.channel]))

    def _assign_common_values_from_channel(self, channel_values: ChannelValues):
        self.color = channel_values.color if self.mode.color_support != ColorSupport.None_ else Color("black")
        self.use_random_color = (
                (self.mode.color_support == ColorSupport.All) and
                (channel_values.color_source & 0x80 != 0))

        self.speed = self.mode.find_speed(channel_values.speed, Speed.Medium)
        self.brightness = self.mode.find_brightness(channel_values.brightness, Brightness.Medium)


class BasicPrismComponent(PrismComponent, ABC):
    def __init__(self, usb: UsbInterface, channel: int):
        super().__init__(usb, BasicPrismMode.Off)
        self._channel: int = channel
        self._reload_values()

    @property
    def channel(self):
        return self._channel

    @property
    def _byte_values(self) -> Sequence[int]:
        try:
            brightness: int = self.mode.brightnesses[self.brightness]
        except KeyError:
            brightness: int = 0

        try:
            speed: int = self.mode.speeds[self.speed]
        except KeyError:
            speed: int = 0x2C

        color_source: int = 0x80 if self.use_random_color else 0x20

        return [self._channel, speed, color_source, self.mode.mode, 0xFF, brightness] + self._color_bytes

    def _reload_values(self):
        channel_values = self._fetch_channel_values()
        self.mode = BasicPrismMode.from_mode(channel_values.mode)
        self._assign_common_values_from_channel(channel_values)
        self.save()


class PrismLogoComponent(BasicPrismComponent):
    def __init__(self, usb: UsbInterface, channel: int):
        super().__init__(usb, channel)


class PrismFanComponent(BasicPrismComponent):
    def __init__(self, usb: UsbInterface, channel: int):
        super().__init__(usb, channel)

        # No hardware getter, so mirageState starts as off due to being unknown
        self.mirage_state: MirageState = MirageState.Off


class PrismRingComponent(PrismComponent):
    def __init__(self, usb: UsbInterface, channel: int):
        try:
            mode = next((mode for mode in PrismRingMode if mode.channel == channel))
        except StopIteration:
            print(f"Received invalid ring channel byte {channel}. Falling back to rainbow mode")
            mode = PrismRingMode.Rainbow

        super().__init__(usb, mode)

        self._morse_text: str = ""
        self._saved_morse_text: str = ""
        self._cached_morse_bytes: Sequence[int] or None = None

        self._reload_values()

    @property
    def channel(self):
        return self.mode.channel

    def save(self):
        super().save()
        self._saved_morse_text = self._morse_text

    @property
    def has_unsaved_changes(self) -> bool:
        if not super().has_unsaved_changes:
            if self.mode == PrismRingMode.Morse:
                return self._morse_text.strip().upper() != self._saved_morse_text.strip().upper()
            else:
                return False

    def _reload_values(self):
        channel_values = self._fetch_channel_values()
        self.mode: PrismRingMode = next((mode for mode in PrismRingMode if mode.channel == channel_values.channel))
        self.direction = RotationDirection(
            channel_values.color_source & 1) if self.mode.supports_direction else RotationDirection.Clockwise
        self._assign_common_values_from_channel(channel_values)
        self._cached_morse_bytes = list(self._fetch_morse_bytes())
        self._morse_text = bytes_to_morse_or_text(self._cached_morse_bytes)
        self.save()

    def _fetch_morse_bytes(self) -> Iterable[int]:
        first_chunk = self._usb.send_bytes([0x52, 0x73, 2])
        second_chunk = self._usb.send_bytes([0x52, 0x73, 3])

        return itertools.chain(first_chunk[4:], second_chunk[4:])

    @property
    def _byte_values(self) -> Sequence[int]:
        try:
            brightness: int = self.mode.brightnesses[self.brightness]
        except KeyError:
            brightness: int = 0x99

        try:
            speed: int = self.mode.speeds[self.speed] if self.mode != PrismRingMode.Morse else 0x6B
        except KeyError:
            speed: int = 0x2C

        if self.mode.color_support == ColorSupport.All and self.use_random_color:
            if self.mode.supports_direction:
                color_source = 0x80 + self.direction.value()
            else:
                color_source = 0
        elif self.mode.supports_direction:
            color_source = self.direction.value()
        else:
            color_source = self.mode.color_source

        return [self.mode.channel, speed, color_source, self.mode.mode, 0xFF, brightness] + self._color_bytes

    @property
    def _morse_bytes(self):
        if self._cached_morse_bytes is None:
            self._cached_morse_bytes = morse_or_text_to_bytes(self._morse_text)
        return self._cached_morse_bytes

    def submit_values(self):
        self._submit_morse_values()
        super().submit_values()

    def _submit_morse_values(self):
        morse_bytes = self._morse_bytes
        first_chunk = itertools.chain([0x51, 0x73, 0, 0], morse_bytes[0:60])
        third_chunk = itertools.chain([0x51, 0x73, 2, 0], morse_bytes[0:60])
        if len(morse_bytes) >= 60:
            second_chunk = itertools.chain([0x51, 0x73, 1, 0], morse_bytes[60:120])
            fourth_chunk = itertools.chain([0x51, 0x73, 3, 0], morse_bytes[60:120])
        else:
            second_chunk = [0x51, 0x73, 1, 0]
            fourth_chunk = [0x51, 0x73, 3, 0]

        self._usb.send_bytes(first_chunk)
        self._usb.send_bytes(second_chunk)
        self._usb.send_bytes(third_chunk)
        self._usb.send_bytes(fourth_chunk)

    @property
    def morse_text(self):
        return self._morse_text

    @morse_text.setter
    def morse_text(self, value: str):
        self._morse_text = value
        self._cached_morse_bytes = None

    @property
    def morse_bytes(self):
        return self._morse_bytes
