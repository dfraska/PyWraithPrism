from py_wraith_prism.usb.hid_device_manager import UsbInterface
from py_wraith_prism.prism_components.prism_components import PrismLogoComponent, \
    PrismComponent, PrismFanComponent, PrismRingComponent
from typing import Sequence, List


class Components(Sequence[PrismComponent]):
    def __init__(self, usb: UsbInterface, data: List[int]):
        self._logo = PrismLogoComponent(usb, data[8])
        self._fan = PrismFanComponent(usb, data[9])
        self._ring = PrismRingComponent(usb, data[10])

        self._values = [self.logo, self.fan, self.ring]

    def __getitem__(self, index):
        return self._values[index]

    def __len__(self):
        return 3

    @property
    def logo(self) -> PrismLogoComponent:
        return self._logo

    @property
    def fan(self) -> PrismFanComponent:
        return self._fan

    @property
    def ring(self) -> PrismRingComponent:
        return self._ring

    def save(self):
        for component in self._values:
            component.save()

    @property
    def has_unsaved_changes(self) -> bool:
        for component in self._values:
            if component.has_unsaved_changes:
                return True
        return False
