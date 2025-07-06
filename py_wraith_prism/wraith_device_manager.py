from py_wraith_prism.usb.hid_device_manager import HidDeviceManager
from py_wraith_prism.wraith_prism import WraithPrism

_VENDOR_ID = 0x2516
_PRODUCT_ID = 0x0051
_IFACE_NUM = 1


class WraithDeviceManager(HidDeviceManager):
    def __init__(self):
        super().__init__(_VENDOR_ID, _PRODUCT_ID, _IFACE_NUM)

    def create_device(self, descriptor=None) -> WraithPrism:
        if descriptor is None:
            device = self._open_first_device()
        else:
            device = self._open_device(descriptor)
        return WraithPrism(device)
