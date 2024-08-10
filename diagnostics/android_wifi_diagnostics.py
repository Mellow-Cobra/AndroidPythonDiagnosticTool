# Standard Imports
import logging
import subprocess
import os


# Local Imports
from android_devices.adb_interface import AdbInterface

logger = logging.getLogger(__name__)

class WifiDiagnostics():
    """Class used for Android device wifi diagnostics"""


    def __init__(self, serial_number):
        self.adb_interface = AdbInterface(serial_number)

    def wifi_level_one_diagnostics(self):
        wifi_status = self.adb_interface.get_wifi_status()

        self.adb_interface.get_wifi_network_info()
        self.adb_interface.get_wifi_internet_status()
        self.adb_interface.run_ping_test()
        self.adb_interface.get_wifi_station_ssid()
        self.adb_interface.get_signal_strength()

    def verify_wifi_radio(self):
        """Method used to verify wifi radio functionality"""
        self.adb_interface.set_global_wifi_off()
        self.adb_interface.set_global_wifi_on()

    def generate_wifi_test_report(self):
        """Method used to generate WiFi test report"""

if __name__ == '''__main__''':
    w = WifiDiagnostics(serial_number=375010008142000055)
    w.wifi_level_one_diagnostics()
    w.verify_wifi_radio()