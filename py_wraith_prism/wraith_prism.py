from contextlib import AbstractContextManager
from types import TracebackType
from typing import Type

from py_wraith_prism.prism_components.components import Components
from py_wraith_prism.prism_components.enums import Speed, Brightness
from py_wraith_prism.prism_components.mirage_state import MirageState
from py_wraith_prism.prism_components.prism_components import PrismLogoComponent, PrismFanComponent, \
    PrismRingComponent, PrismComponent
from py_wraith_prism.prism_components.prism_mode import BasicPrismMode, \
    PrismRingMode
from py_wraith_prism.usb.hid_device_manager import UsbInterface


SECONDS_PER_MILLISECOND = 1 / 1000


class WraithPrism(AbstractContextManager):
    def __init__(self, usb: UsbInterface):
        self._usb = usb

        # Power on
        self.power_on()
        self._restore()
        self.apply()

        # Request channel data
        data = usb.send_bytes([0x52, 0xA0, 1, 0, 0, 3])
        self._components = Components(usb, data)

    def submit_component(self, component: PrismComponent):
        component.submit_values()
        self._assign_channels()
        self.apply()

    def submit_components(self, *argv):
        for component in argv:
            component.submit_values()
        if any(argv):
            self._assign_channels()
            self.apply()

    def submit_all_components(self):
        for component in self._components:
            component.submit_values()
        self._assign_channels()
        self.apply()

    def save(self):
        self._usb.send_bytes([0x50, 0x55])
        self._components.save()

    def _restore(self):
        self._usb.send_bytes([0x50])

    @property
    def logo(self) -> PrismLogoComponent:
        return self._components.logo

    @property
    def fan(self) -> PrismFanComponent:
        return self._components.fan

    @property
    def ring(self) -> PrismRingComponent:
        return self._components.ring

    @property
    def has_unsaved_changes(self) -> bool:
        return self._components.has_unsaved_changes

    @property
    def enso(self) -> bool:
        return self._usb.send_bytes([0x52, 0x96])[4] == 0x10

    @enso.setter
    def enso(self, value: bool):
        if value:
            self._usb.send_bytes([0x51, 0x96, 0, 0, 0x10])
            self.save()
        else:
            self._usb.send_bytes([0x51, 0x96])

    def _assign_channels(self):
        pkt = [0x51, 0xA0, 1, 0, 0, 3, 0, 0, self.logo.channel, self.fan.channel] + [self.ring.channel] * 15
        self._usb.send_bytes(pkt)

    def apply(self):
        self._usb.send_bytes([0x51, 0x28, 0, 0, 0xE0])

    def request_firmware_version(self) -> str:
        response = self._usb.send_bytes([0x12, 0x20])
        version = bytes(filter(lambda b: b != 0, response[8:34])).decode().lower()
        return version

    def reset_to_default(self):
        self.enso = False

        # Reset all the component settings to default
        self.fan.mode = self.logo.mode = BasicPrismMode.Cycle
        self.ring.mode = PrismRingMode.Rainbow
        self.fan.speed = self.logo.speed = self.ring.speed = Speed.Medium
        self.fan.brightness = self.logo.brightness = self.ring.brightness = Brightness.High
        self.fan.mirage_state = MirageState.Default

        for component in self._components:
            component.submit_values()

        self._assign_channels()
        self.apply()

    def __exit__(self, __exc_type: Type[BaseException] or None, __exc_value: BaseException or None,
                 __traceback: TracebackType or None) -> bool or None:
        return self._usb.__exit__(__exc_type, __exc_value, __traceback)

    def power_on(self):
        self._usb.send_bytes([0x41, 0x80])

    def power_off(self):
        self._usb.send_bytes([0x41, 0x03])

    def close(self):
        self._usb.close()
