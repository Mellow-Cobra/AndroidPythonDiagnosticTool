# Standard Imports
import logging

# Internal Imports
import subprocess
from .gpu_base import GpuBuilder
from android_devices.adb_interface import AdbInterface

logger = logging.getLogger(__name__)

class Adreno(GpuBuilder):
    """Class used for Adreno GPU Model builder"""

    def __init__(self, adb):
        """Constructor"""
        self.adb_int = adb

    def get_gpu_temperature(self):
        """Method used to get GPU temperature"""
        gpu_temp_exposed_paths = ["/sys/class/kgsl/kgsl-3d0/temp",
                                  "/sys/class/thermal/thermal_zone*"
        ]
        for _, path in enumerate(gpu_temp_exposed_paths):
            temperature = float(self.adb_int.run_adb_command(f"cat {path}")) / 1000
            logger.info(f"Adreno GPU Temperature is logged at: {temperature} Celsius")

            return temperature


    def get_gpu_frequency(self):
        """Method used to get GPU temperature"""
        frequency_counter_exposed_paths = ["/sys/class/kgsl/kgsl-3d0/gpuclk"]

        for _, path in enumerate(frequency_counter_exposed_paths):
            frequency = float(self.adb_int.run_adb_command(f"cat {path}")) / 1000
            logger.info(f"Adreno GPU core frequency is logged at: {frequency} Hz")

