import os

_udev_file_path = "/etc/udev/rules.d/60-wraith-prism.rules"
_rule = 'SUBSYSTEM=="usb", ATTR{idVendor}=="2516", ATTR{idProduct}=="0051", TAG+="uaccess", TAG+="udev-acl"'


def add_udev_rule():
    if os.geteuid() == 0:
        try:
            with open(_udev_file_path, "w") as f:
                f.write(_rule)
                print(f'Created "{_udev_file_path}"')
                print('udev should apply the new rule automatically. If not, try running "sudo udevadm trigger".')
        except OSError:
            print(f'Failed to create "{_udev_file_path}"')
            raise
    else:
        print("This command must be run as root in order to create udev rule. (sudo python add-udev-rule.py)")
        print(f'You can also do this manually by creating "{_udev_file_path}" with following content:')
        print(_rule)


if __name__ == "__main__":
    add_udev_rule()
