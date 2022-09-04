from colour import Color

from py_wraith_prism.prism_components.enums import Brightness, Speed
from py_wraith_prism.prism_components.prism_mode import PrismRingMode, BasicPrismMode
from py_wraith_prism.wraith_device_manager import WraithDeviceManager

if __name__ == '__main__':
    device_manager = WraithDeviceManager()

    with device_manager.create_device() as prism:
        version = prism.request_firmware_version()
        print(f"Prism version: {version}")

        print(f"morse text (before set): {prism.ring.morse_text}")

        prism.ring.mode = PrismRingMode.Morse
        prism.ring.morse_text = "abc"
        prism.ring.color = Color("red")
        prism.ring.brightness = Brightness.High

        prism.fan.mode = BasicPrismMode.Static
        prism.fan.color = Color("green")
        prism.fan.brightness = Brightness.High

        prism.logo.mode = BasicPrismMode.Breathe
        prism.logo.speed = Speed.Slow
        prism.logo.color = Color("blue")
        prism.logo.brightness = Brightness.High

        print(f"morse text (after set): {prism.ring.morse_text}")

        prism.submit_all_components()
        prism.save()
