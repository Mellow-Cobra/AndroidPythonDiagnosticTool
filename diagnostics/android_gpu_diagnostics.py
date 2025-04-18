# Standard Imports

import logging

# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *

logger = logging.getLogger(__name__)


class AndroidGPUDiagnostics:
    """GPU diagnostics class"""

    def __init__(self, device_serial_number, configuration):
        """Constructor"""
        self.adb_interface = AdbInterface(device_serial_number)
        self.device_serial_number = device_serial_number
        self.configuration = configuration

    def gpu_level_zero_diagnostics(self):
        """GPU level one diagnostics"""
        gpu = self.adb_interface.get_gpu_information()
        print(gpu)

    def gpu_level_one_diagnostics(self):
        """GPU level two diagnostics"""
        pass

