# Standard Imports
import subprocess
import os


# Local Imports
from android_devices.adb_interface import AdbInterface


class WifiDiagnostics():
    """Class used for Android device wifi diagnostics"""


    def __init__(self, serial_number):
        self.adb_interface = AdbInterface(serial_number)

    def wifi_level_one_diagnostics(self):
        self.adb_interface.get_wifi_status()
        self.adb_interface.get_wifi_network_info()



if __name__ == '''__main__''':
    w = WifiDiagnostics(serial_number=375010008142000055)
    w.wifi_level_one_diagnostics()