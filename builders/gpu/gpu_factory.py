# Standard Imports
import logging
import re
import subprocess


# Internal Imports
from .gpu_base import GpuBuilder
from android_devices.adb_interface import AdbInterface
from .adreno_builder import Adreno
from core.constants import *

logger = logging.getLogger(__name__)


class  GpuFactory(GpuBuilder):
    """GPU Factory class to detect GPU and apply appropriate settings"""

    @staticmethod
    def detect_gpu(serial_number):
        """Method used to detect GPU model and instantiate builder object"""
        logger.info("Capturing GPU model information...")
        adb_int = AdbInterface(serial_number)
        try:
            gpu_info = adb_int.run_adb_command("getprop ro.hardware.egl")
            logger.info(gpu_info)
            return Adreno(adb_int)

        except (FileNotFoundError, ConnectionError, ValueError) as error:
            logger.info(f"Could not connect to Device Under Test. Encountered {error}")
            raise error

