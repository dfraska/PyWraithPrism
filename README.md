# About
PyWraithPrism allows control of the AMD Wraith Prism CPU fan RGB LEDs from within Python from "any" platform
(specifically tested on Windows, but this should also work on Linux or any other platform that supports
[hidapi](https://pypi.org/project/hidapi/)).

Other projects exist for controlling the Wraith Prism cooler (see the [Acknowledgements](#Acknowledgements) section for
some examples). These are either written for other platforms, or are not feature-complete enough for my uses.

# Installation
Install the package using pip
```python -m pip install git+https://github.com/dfraska/PyWraithPrism#egg=py_wraith_prism```
or pipenv
```pipenv install git+https://github.com/dfraska/PyWraithPrism#egg=py_wraith_prism```

On Linux, add a udev rule to allow user-mode access to the USB device. You can do this automatically by running the
included
[script](https://github.com/dfraska/PyWraithPrism/blob/main/py_wraith_prism/add_udev_rule.py)
as sudo
```sudo python -m py_wraith_prism/add_udev_rule```

# Usage
See the examples under [tests](https://github.com/dfraska/PyWraithPrism/blob/main/tests/) for a basic usage example.

The primary methods for controlling the LEDs are through the ring, fan, and logo components. When you're done modifying
settings, call ```prism.submit_all_components()``` to apply the current settings, and ```prism.save()``` to save the
values to the hardware.

# Acknowledgements
- [Campbell Jones (serebit)](https://github.com/serebit): [Wrath Master](https://github.com/serebit/wraith-master), a 
GUI application for controlling the Wraith Prism in Linux, primarily written in Kotlin. The architecture of PyWrathPrism
was heavily influenced by this project.
- [gfduszynski](https://github.com/gfduszynski): [cm-rgb](https://github.com/gfduszynski/cm-rgb) was used as a
reference, especially when working on the HID interface and debugging.
- [Adam Honse](https://gitlab.com/CalcProgrammer1): [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB), particularly
the [AMD Wraith Prism reference](https://gitlab.com/CalcProgrammer1/OpenRGB/-/wikis/AMD-Wraith-Prism)
