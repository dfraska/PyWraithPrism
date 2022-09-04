from typing import Any, Generator

import hid
from hid import device as hid_device

from py_wraith_prism.usb.usb_interface import UsbInterface


class HidDeviceManager:
    def __init__(self, vendor_id, product_id, interface_number, request_size: int = 64):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_number = interface_number
        self._request_size = request_size
        self._device = hid_device()

    def _enumerate_devices(self) -> Generator[Any, Any, None]:
        for descriptor in hid.enumerate(self.vendor_id, self.product_id):
            if descriptor['interface_number'] == self.interface_number:
                yield descriptor
    
    def _create_interface(self) -> UsbInterface:
        descriptors = self._enumerate_devices()
        try:
            descriptor = next(descriptors)
        except StopIteration:
            # No descriptors were found
            raise IOError("Failed to find a matching device.")
        
        try:
            self._device.open_path(descriptor["path"])
            return UsbInterface(self._device, self._request_size)
        except OSError as e:
            raise IOError("Failed to open the device.") from e
            