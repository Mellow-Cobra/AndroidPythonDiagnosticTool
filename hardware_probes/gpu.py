# Standard Imports
import logging
import re

# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *


logger = logging.getLogger(__name__)


class AdbGpuProbe:
    """A class used to probe Android device GPU via ADB shell commands"""
    def __init__(self, device_serial_number):
        """Constructor"""
        self.adb_shell = AdbInterface(device_serial_number)



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

    def enable_super_user_mode(self):
        """Method used to enable super user mode"""
        logger.info("Enabling super user mode")
        super_user_mode = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                          "root"], capture_output=True)
        super_user_mode.stdout.decode("utf-8")

    def disable_wifi_service(self):
        """Method used to disable WiFi radio"""
        logger.info("Disabling WiFi service")
        disabled_wifi = subprocess.run(["adb", "shell", "svc wifi disable"], capture_output=True)

        disabled_wifi = disabled_wifi.stdout.decode("utf-8")

        return disabled_wifi

    def enable_wifi_service(self):
        """Method used to enable WiFi radio"""
        logger.info("Enabling WiFi Service")
        enabled_wifi = subprocess.run(["adb", "shell", "svc wifi enable"], capture_output=True)

        enabled_wifi = enabled_wifi.stdout.decode("utf-8")

        return enabled_wifi

    def enable_nfc_service(self):
        """Method used to enable NFC radio"""
        logger.info("Enabling NFC service")
        enabled_nfc = subprocess.run(["adb", "shell", "svc nfc enable"])

        enabled_nfc = enabled_nfc.stdout.decode("utf-8")

        return enabled_nfc



    def get_cpu_min_speed(self):
        """Method used to get cpu min speed"""
        logger.info("Capturing minimum CPU speeds...")
        cpu_min_speeds = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                         "shell", "cat", "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_min_freq"],
                                        capture_output=True )
        cpu_min_speeds = cpu_min_speeds.stdout.decode("utf-8").splitlines()

        return cpu_min_speeds



        return serial_numbers

    def get_gpu_information(self):
        """Method used to get GPU model"""
        logger.info("Capturing GPU model information...")
        pattern = (r"GLES:\s*(?P<vendor>\w+),\s*(?P<model>.+?),\s*"
                    r"(?P<api_name>(Open\s*GL\s*ES|Vulkan|OpenCL|Metal))\s+"
                    r"(?P<gl_version>[\d.]+) V@(?P<driver_version>[\d.]+)")
        gpu_information = self.adb_shell.run_adb_command("dumpsys SurfaceFlinger | grep GLES")
        match = re.search(pattern, gpu_information)
        if match:
            gpu_info = match.groupdict()
            logger.info(gpu_info)
        else:
            gpu_info = NOT_AVAILABLE
            logger.info("Could not determine GPU information.")


        return gpu_info
