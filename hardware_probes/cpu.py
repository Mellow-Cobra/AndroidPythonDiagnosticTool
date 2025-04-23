# Standard Imports
import logging
import re

from typing import Optional

# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *


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

    def get_cpu_architecture(self):
        """Method used to get CPU architecture"""
        logger.info("Retrieving CPU Architecture.")
        cpu_arch = self._adb_shell.run_adb_command("getprop ro.product.cpu.abi")

        return cpu_arch

    def get_cpu_governor(self):
        """Method used to check CPU governor"""
        logger.info("Checking CPU governor.")
        cpu_governor_dictionary = {}
        cpu_governor_output = self._adb_shell.run_adb_command("cat /sys/devices/system/cpu/cpu*"
                                                              "/cpufreq/scaling_governor").split("\r\n")
        for index, cpu_governor in enumerate(cpu_governor_output):
            cpu_governor_dictionary.update({f"cpu{index} governor": cpu_governor})

        return cpu_governor_dictionary


    def check_cpus_online(self):
        """Method used to check which CPUs are online"""
        logger.info("Checking which CPUs are online.")
        cpus_online_output = (self._adb_shell.run_adb_command("cat /sys/devices/system/cpu/cpu[0-9]*/online")
                              .split("\r\n"))
        cpus_online = {}
        for index, cpu_status in enumerate(cpus_online_output):
            cpus_online.update({f"cpu{index} online_status": f"{cpu_status}"})


        return cpus_online


    def get_cpu_hardware(self) -> Optional[str]:
        """Method used to get CPU information"""
        cpu_hardware = self._adb_shell.run_adb_command("cat /proc/cpuinfo")
        regex_pattern = r"Hardware\s*\:\s[A-Za-z0-9\s\-\_\@\#\!\.\$\,]+"
        match = re.search(pattern=regex_pattern, string=cpu_hardware)
        if match:
            logger.info(f"CPU Hardware manufacturer: {match.group()}")
            return match.group()
        else:
            return NOT_AVAILABLE