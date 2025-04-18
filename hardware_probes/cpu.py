# Standard Imports
import logging
import re

# Local Imports
from android_devices.adb_interface import AdbInterface


logger = logging.getLogger(__name__)


class AdbCpuProbe:
    """Class used to probe CPU over adb shell at low level"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_shell = AdbInterface(device_serial_number)


    def get_cpu_temperatures(self):
        """Method used to get CPU temperatures"""
        logger.info("Retrieving CPU temperatures")
        temperatures = list()
        thermal_service = self._adb_shell.run_adb_command("dumpsys thermalservice | grep CPU")

        temp_regex = r"\bmValue\b=([0-9])*\.([0-9])*"
        for _, temp in enumerate(thermal_service):

            match = re.search(pattern=temp_regex, string=temp)
            if match:
                temperatures.append(float(match.group().strip("mValue=")))
                print(temperatures)

        return temperatures


    def get_cpu_frequencies(self):
        """Method used to get CPU frequencies"""
        logger.info("Retrieving current CPU frequencies")
        cpu_frequencies = list()
        available_cpus = self._adb_shell.run_adb_command("find /sys/devices/system/cpu/ -name cpu[0-9]*")

        available_cpus = sorted(available_cpus.stdout.decode("utf-8").splitlines())

        for index, cpu_directory in enumerate(available_cpus):
            cpu_freq = self._adb_shell.run_adb_command(f"cat {cpu_directory}/cpufreq/cpuinfo_cur_freq")
            cpu_freq = float(cpu_freq.stdout.decode("utf-8").strip('\r\n'))
            cpu_frequencies.append(cpu_freq)

        return cpu_frequencies


    def get_cpu_max_speed(self):
        """Method used to get cpu max speed"""
        logger.info("Capturing CPU maximum speed...")
        cpu_max_speeds = self._adb_shell.run_adb_command("cat "
                                                         "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_max_freq")
        cpu_max_speeds = cpu_max_speeds.stdout.decode("utf-8").splitlines()

        return cpu_max_speeds

    def get_cpu_min_speed(self):
        """Method used to get cpu min speed"""
        logger.info("Capturing minimum CPU speeds...")
        cpu_min_speeds = self._adb_shell.run_adb_command("cat"
                                                         "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_min_freq")
        cpu_min_speeds = cpu_min_speeds.stdout.decode("utf-8").splitlines()

        return cpu_min_speeds
