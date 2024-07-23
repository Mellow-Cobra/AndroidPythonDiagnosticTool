# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *

class AndroidCpuDiagnostics:
    """Android CPU Diagnostics class"""

    def __init__(self, serial_number):
        """Constructor"""
        self.adb_interface = AdbInterface(serial_number)


    def run_cpu_diagnostics(self):
        """Method used to run CPU diagnostics"""
        self.adb_interface.enable_super_user_mode()
        cpu_temperatures = self.adb_interface.get_cpu_temperatures()
        cpu_frequencies = self.adb_interface.get_cpu_frequencies()
        cpu_clock_diag_results = self.evaluate_cpu_clock_speed_diagnostics(cpu_frequencies)
        cpu_temp_diag_results = self.evaluate_cpu_temperatures(cpu_temperatures)

        print(cpu_clock_diag_results)
        print(cpu_temp_diag_results)

    def evaluate_cpu_clock_speed_diagnostics(self, cpu_frequencies):
        """Method used to evaluate hardware diagnostics"""
        min_frequencies = self.adb_interface.get_cpu_min_speed()
        max_frequencies = self.adb_interface.get_cpu_max_speed()
        cpu_freq_diag_test_results = list()
        for index, frequency in enumerate(cpu_frequencies):
            if max_frequencies[index] >= frequency <= min_frequencies[index]:
                cpu_freq_diag_test_status = {"CPU": index,
                                             "Max_Frequency": max_frequencies[index],
                                             "Frequency": frequency,
                                             "Min_Frequency": min_frequencies[index],
                                             "Units": MHZ
                                             }
                cpu_freq_diag_test_results.append(cpu_freq_diag_test_results)
            else:
                cpu_freq_diag_test_status  = {"CPU": index,
                                              "Max_Frequency": max_frequencies[index],
                                              "Frequency": frequency,
                                              "Min_Frequency": min_frequencies[index],
                                              "Units": MHZ
                                              }
                cpu_freq_diag_test_results.append(cpu_freq_diag_test_status)

        return cpu_freq_diag_test_results

    def evaluate_cpu_temperatures(self, cpu_temperatures):
        """Method used to evaluate cpu temperatures"""
        cpu_test_results = list()
        for index, temperature in enumerate(cpu_temperatures):
            if temperature < MAX_TEMPERATURE_LIMIT_C:
                cpu_temperature_test_status = {"CPU": index,
                                               "Max_Temperature": MAX_TEMPERATURE_LIMIT_C,
                                               "Temperature Diagnostic Read out": temperature,
                                               "Diagnostic_Result": CPU_TEMP_SAFE,
                                               "Units": CELSIUS
                                               }
                cpu_test_results.append(cpu_temperature_test_status)
            else:
                cpu_temperature_test_status = {"CPU": index,
                                               "Max_Temperature": MAX_TEMPERATURE_LIMIT_C,
                                               "Temperature Diagnostic Read out": temperature,
                                               "Diagnostic_Result": CPU_THROTTLE_OT,
                                               "Units": CELSIUS}
                cpu_test_results.append(cpu_temperature_test_status)

            return cpu_test_results
