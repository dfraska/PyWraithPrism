from typing import Any, Generator, Iterable

import hid
from hid import device as hid_device


class HidDeviceManager:
    def __init__(self, vendor_id: int | Iterable[int], product_id: int | Iterable[int],
                 interface_number: int | Iterable[int]):
        if not hasattr(vendor_id, '__iter__'):
            vendor_id = (vendor_id,)
        self._vendor_ids = vendor_id

        if not hasattr(product_id, '__iter__'):
            product_id = (product_id,)
        self._product_ids = product_id

        if not hasattr(interface_number, '__iter__'):
            interface_number = (interface_number,)
        self.interface_numbers = interface_number

        self._device = hid_device()

    def _enumerate_devices(self) -> Generator[Any, Any, None]:
        for vendor_id in self._vendor_ids:
            for product_id in self._product_ids:
                for descriptor in hid.enumerate(vendor_id=vendor_id, product_id=product_id):
                    if descriptor['interface_number'] in self.interface_numbers:
                        yield descriptor

    def _open_first_device(self) -> hid_device:
        descriptors = self._enumerate_devices()
        try:
            descriptor = next(descriptors)
        except StopIteration:
            # No descriptors were found
            raise IOError("Failed to find a matching device.")

        try:
            self._device.open_path(descriptor["path"])
            return self._device
        except OSError as e:
            raise IOError("Failed to open the device.") from e
