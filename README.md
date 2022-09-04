# About
PyWraithPrism allows control of the AMD Wraith Prism CPU fan RGB LEDs from within Python.

Other projects exist for controlling the Wraith Prism cooler (see the [Acknowledgements](#Acknowledgements) section 
for some examples). Other options I found were either written for other platforms, or are not feature-complete enough for my uses.

# Usage
See the example under tests/test.py for a basic usage example. The primary methods for controlling the LEDs are 
through the ring, fan, and logo components. When you're done modifying settings, call
```prism.submit_all_components()``` to apply the current settings, and ```prism.save()``` to save the values to the 
hardware.

# Acknowledgements
- [Campbell Jones (serebit)](https://github.com/serebit):
[Wrath Master](https://github.com/serebit/wraith-master), a GUI application for controlling the Wraith Prism in Linux,
primarily written in Kotlin. The architecture of PyWrathPrism was heavily influenced by this project.
- [gfduszynski](https://github.com/gfduszynski): [cm-rgb](https://github.com/gfduszynski/cm-rgb) was used as a 
  reference, especially when working on the HID interface and debugging. 
- [Adam Honse](https://gitlab.com/CalcProgrammer1): [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB), particularly
the [AMD Wraith Prism reference](https://gitlab.com/CalcProgrammer1/OpenRGB/-/wikis/AMD-Wraith-Prism)
- 


