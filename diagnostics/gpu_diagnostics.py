# Standard Imports

import logging

# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *

logger = logging.getLogger(__name__)


class AndroidGPUDiagnostics:
    """GPU diagnostics class"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        self.adb_interface = AdbInterface(serial_number)
        self.serial_number = serial_number
        self.configuration = configuration

    def gpu_level_one_diagnostics(self):
        """GPU level one diagnostics"""
        gpu_model_number = self.adb_interface.get_gpu_model()
        print(gpu_model_number)

