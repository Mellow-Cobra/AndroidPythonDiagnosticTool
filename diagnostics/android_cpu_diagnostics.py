# Local Imports
import csv
import datetime
import os
from hardware_probes.cpu import AdbCpuProbe
from core.constants import *

# Third Part Imports


class AndroidCpuDiagnostics:
    """Android CPU Diagnostics class"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        self._adb_cpu_probe = AdbCpuProbe(serial_number)
        self.configuration = configuration
        self.test_results = []

    def run_cpu_diagnostics(self):
        """Method used to run CPU diagnostics"""
        self.level_zero_cpu_diagnostics()
        # self.evaluate_cpu_temperatures()
        # self.evaluate_cpu_clock_speed_diagnostics()
        # self.generate_cpu_diagnostic_test_report()

    def level_zero_cpu_diagnostics(self):
        """Method used to run level zero CPU diagnostics"""
        self._adb_cpu_probe.get_cpu_architecture()
        self._adb_cpu_probe.get_cpu_hardware()
        self._adb_cpu_probe.get_cpu_governor()
        self._adb_cpu_probe.check_cpus_online()


    def evaluate_cpu_clock_speed_diagnostics(self):
        """Method used to evaluate hardware diagnostics"""
        min_frequencies = self._adb_cpu_probe.get_cpu_min_speed()
        max_frequencies = self._adb_cpu_probe.get_cpu_max_speed()
        cpu_frequencies = self._adb_cpu_probe.get_cpu_frequencies()
        self.test_results.append(CPU_FREQUENCY_DIAGNOSTIC_HEADER)
        for index, frequency in enumerate(cpu_frequencies):
            if float(max_frequencies[index]) >= frequency >= float(min_frequencies[index]):
                cpu_freq_diag_test_status = [index, min_frequencies[index], frequency, max_frequencies[index],
                                             MHZ, CPU_IN_SPEC, PASS]
                self.test_results.append(cpu_freq_diag_test_status)
            else:
                cpu_freq_diag_test_status = [index, min_frequencies[index], frequency, max_frequencies[index],
                                             MHZ, CPU_FREQ_NOT_IN_SPEC, FAIL]
                self.test_results.append(cpu_freq_diag_test_status)

    def evaluate_cpu_temperatures(self):
        """Method used to evaluate cpu temperatures"""
        cpu_temperatures = self._adb_cpu_probe.get_cpu_temperatures()
        self.test_results.append(CPU_TEMPERATURE_DIAGNOSTIC_HEADER)
        for index, temperature in enumerate(cpu_temperatures):
            if MIN_TEMPERATURE_LIMIT <= float(temperature) < MAX_TEMPERATURE_LIMIT_C:
                cpu_temperature_test_status = [index, MAX_TEMPERATURE_LIMIT_C, temperature, MIN_TEMPERATURE_LIMIT,
                                               CELSIUS, CPU_NO_THROTTLE , PASS]
                self.test_results.append(cpu_temperature_test_status)
            else:
                cpu_temperature_test_status = [index, MAX_TEMPERATURE_LIMIT_C, temperature, MIN_TEMPERATURE_LIMIT,
                                               CELSIUS, CPU_THROTTLE_OT, FAIL]
                self.test_results.append(cpu_temperature_test_status)


    def generate_cpu_diagnostic_test_report(self):
        """Method used to generate test report for CPU diagnostics"""
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        os.chdir(self.configuration[TEST_SETTINGS][TEST_RESULTS])
        with open(f'cpu_diagnostics_{time_stamp}.csv', mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(self.test_results)

