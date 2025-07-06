import itertools
from builtins import bytearray
from contextlib import AbstractContextManager
from types import TracebackType
from typing import List, Type, Iterable

from hid import device as hid_device


class WraithUsbInterface(AbstractContextManager):
    def __init__(self, device: hid_device, request_size: int = 64):
        self._device: hid_device = device
        self._request_size = request_size

    def __exit__(self, __exc_type: Type[BaseException] or None, __exc_value: BaseException or None,
                 __traceback: TracebackType or None) -> bool or None:
        self.close()
        return None

    def close(self):
        self._device.close()

    def send_bytes(self, values: Iterable[int], filler: int = 0) -> List[int]:
        values = bytearray(itertools.chain([0], values))
        if len(values) > self._request_size + 1:
            raise ValueError()

        remaining = self._request_size - len(values) + 1
        values.extend([filler] * remaining)

        self._device.write(values)
        result = self._device.read(self._request_size)
        return result
