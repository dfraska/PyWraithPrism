from py_wraith_prism.usb.hid_device_manager import HidDeviceManager
from py_wraith_prism.wraith_prism import WraithPrism

_VENDOR_ID = 0x2516
_PRODUCT_ID = 0x0051
_PRODUCT_STR = 'CYRM02p0303h00E0r0100'
_IFACE_NUM = 1


class WraithDeviceManager(HidDeviceManager):
    def __init__(self):
        super().__init__(_VENDOR_ID, _PRODUCT_ID, _IFACE_NUM)

    def create_device(self) -> WraithPrism:
        return WraithPrism(super()._create_interface())
