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
