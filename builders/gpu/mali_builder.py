# Standard Import
import pythonjsonlogger

# Internal Imports
from .gpu_base import GpuBuilder


class Mali(GpuBuilder):
    """Class used for Mali GPU Model builder"""

    def __init__(self, adb):
        """Constructor"""
        self.adb_int = adb


    def get_gpu_temperature(self):
        """Method used to get GPU temperature from Mali GPU"""
        exposed_temperature_path = [""]

    def get_gpu_frequency(self):
        """Method used to get GPU frequency from Mali GPU"""
        pass