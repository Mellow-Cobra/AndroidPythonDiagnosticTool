import subprocess
import re

# Local Imports
from constants import *

class AdbInterface:
    """Class used to interface with Android Device over ADB"""


    def __init__(self):
        """Constructor"""
        self.serial_number = "R58N33K32MV"

    def get_battery_level(self):
        """Method used to pull battery diagnostics from android phone"""
        battery_level = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                "shell", "dumpsys", "battery", "| grep level"], capture_output=True)
        battery_level = battery_level.stdout.decode("utf-8")
        battery_level_regex = r"\blevel\b:\s\d*"
        match = re.search(pattern=battery_level_regex, string=battery_level)
        if match:
            print(match.group())
        else:
            return NOT_AVAILABLE

        return battery_level

    def display_connected_android_devices(self):
        """Method used to display currently connected Android devices"""
        connected_devices = subprocess.run(["adb", "devices"], capture_output=True)

        connected_devices = connected_devices.stdout.decode("utf-8")

        return connected_devices

    def disable_wifi_service(self):
        """Method used to disable WiFi radio"""
        disabled_wifi = subprocess.run(["adb", "shell", "svc wifi disable"], capture_output=True)

        disabled_wifi = disabled_wifi.stdout.decode("utf-8")

        return disabled_wifi

    def enable_wifi_service(self):
        """Method used to enable WiFi radio"""
        enabled_wifi = subprocess.run(["adb", "shell", "svc wifi enable"], capture_output=True)

        enabled_wifi = enabled_wifi.stdout.decode("utf-8")

        return enabled_wifi

    def enable_nfc_service(self):
        """Method used to enable NFC radio"""
        enabled_nfc = subprocess.run(["adb", "shell", "svc nfc enable"])

        enabled_nfc = enabled_nfc.stdout.decode("utf-8")

        return enabled_nfc