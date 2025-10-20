

# Internal Imports
import subprocess
from .gpu_base import GpuBuilder
from android_devices.adb_interface import AdbInterface


class Adreno(GpuBuilder):
    """Class used for Adreno GPU Model builder"""

    def __init__(self, adb):
        """Constructor"""
        self.adb_int = adb

    def get_gpu_temperature(self):
        """Method used to get GPU temperature"""
        pass

    def get_gpu_frequency(self):
        """Method used to get GPU temperature"""
        pass

