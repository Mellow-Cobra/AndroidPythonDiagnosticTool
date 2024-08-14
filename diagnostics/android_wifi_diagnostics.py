# Standard Imports
import csv
import datetime
import logging
import os


# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *


logger = logging.getLogger(__name__)

class WifiDiagnostics():
    """Class used for Android device wifi diagnostics"""


    def __init__(self, serial_number, configuration):
        self.adb_interface = AdbInterface(serial_number)
        self.device_serial = serial_number
        self.configuration = configuration
        self.wifi_diag_level_one_results = list()

    def run_wifi_diagnostics(self):
        """Method used to run wifi diagnostics"""
        self.wifi_level_one_diagnostics()
        self.generate_wifi_test_report()

    def wifi_level_one_diagnostics(self):
        """Method used to run level one Diagnostics"""
        self.wifi_diag_level_one_results.append(WIFI_DIAG_HEADER)
        wifi_radio_status = self.adb_interface.get_wifi_radio_status()
        wifi_network_status = self.adb_interface.get_wifi_network_info()
        #self.adb_interface.get_wifi_internet_status()
        #self.adb_interface.run_ping_test()
        #self.adb_interface.get_wifi_station_ssid()
        #self.adb_interface.get_signal_strength()
        self.wifi_diag_level_one_results.append([wifi_radio_status, wifi_network_status])

    def verify_wifi_radio(self):
        """Method used to verify wifi radio functionality"""
        self.adb_interface.set_global_wifi_off()
        self.adb_interface.set_global_wifi_on()

    def generate_wifi_test_report(self):
        """Method used to generate WiFi test report"""
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        os.chdir(self.configuration[TEST_SETTINGS][TEST_RESULTS])
        with open(f'wifi_diagnostics_{self.device_serial}_{time_stamp}.csv', mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(self.wifi_diag_level_one_results)

if __name__ == '''__main__''':
    w = WifiDiagnostics(serial_number=375010008142000055)
    w.wifi_level_one_diagnostics()
    w.verify_wifi_radio()