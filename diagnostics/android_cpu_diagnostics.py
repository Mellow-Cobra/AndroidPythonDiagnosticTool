# Local Imports
import csv
from android_devices.adb_interface import AdbInterface
from constants import *


# Third Part Imports
import pandas as pd

class AndroidCpuDiagnostics:
    """Android CPU Diagnostics class"""

    def __init__(self, serial_number):
        """Constructor"""
        self.adb_interface = AdbInterface(serial_number)
        self.test_results = []


    def run_cpu_diagnostics(self):
        """Method used to run CPU diagnostics"""
        self.adb_interface.enable_super_user_mode()
        self.evaluate_cpu_temperatures()
        self.evaluate_cpu_clock_speed_diagnostics()
        self.generate_cpu_diagnostic_test_report()

    def evaluate_cpu_clock_speed_diagnostics(self):
        """Method used to evaluate hardware diagnostics"""
        min_frequencies = self.adb_interface.get_cpu_min_speed()
        max_frequencies = self.adb_interface.get_cpu_max_speed()
        cpu_frequencies = self.adb_interface.get_cpu_frequencies()
        for index, frequency in enumerate(cpu_frequencies):
            if max_frequencies[index] >= frequency <= min_frequencies[index]:
                cpu_freq_diag_test_status = {"CPU": index,
                                             "Max_Frequency": max_frequencies[index],
                                             "Frequency": frequency,
                                             "Min_Frequency": min_frequencies[index],
                                             "Units": MHZ
                                             }
                self.test_results.append(cpu_freq_diag_test_status)
            else:
                cpu_freq_diag_test_status  = {"CPU": index,
                                              "Max_Frequency": max_frequencies[index],
                                              "Frequency": frequency,
                                              "Min_Frequency": min_frequencies[index],
                                              "Units": MHZ
                                              }
                self.test_results.append(cpu_freq_diag_test_status)


    def evaluate_cpu_temperatures(self):
        """Method used to evaluate cpu temperatures"""
        cpu_temperatures = self.adb_interface.get_cpu_temperatures()
        for index, temperature in enumerate(cpu_temperatures):
            if temperature < MAX_TEMPERATURE_LIMIT_C:
                cpu_temperature_test_status = {"CPU": index,
                                               "Max_Temperature": MAX_TEMPERATURE_LIMIT_C,
                                               "Temperature Diagnostic Read out": temperature,
                                               "Diagnostic_Result": CPU_TEMP_SAFE,
                                               "Units": CELSIUS
                                               }
                self.test_results.append(cpu_temperature_test_status)
            else:
                cpu_temperature_test_status = {"CPU": index,
                                               "Max_Temperature": MAX_TEMPERATURE_LIMIT_C,
                                               "Temperature Diagnostic Read out": temperature,
                                               "Diagnostic_Result": CPU_THROTTLE_OT,
                                               "Units": CELSIUS}
                self.test_results.append(cpu_temperature_test_status)



    def generate_cpu_diagnostic_test_report(self):
        """Method used to generate test report for CPU diagnostics"""
        cpu_df = pd.DataFrame(self.test_results)
        print(cpu_df)


