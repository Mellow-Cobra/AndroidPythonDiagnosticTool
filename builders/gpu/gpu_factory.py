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
            pattern = (r"GLES:")
            gpu_information = adb_int.run_adb_command("dumpsys SurfaceFlinger | grep GLES")
            match = re.search(pattern, gpu_information)
            if match:
                gpu_info = match.groupdict()

                logger.info(gpu_info)
                return Adreno(adb_int)
            else:
                gpu_info = NOT_AVAILABLE
                logger.info("Could not determine GPU information.")
        except (FileNotFoundError, ConnectionError, ValueError) as error:
            logger.info(f"Could not connect to Device Under Test. Encountered {error}")
            raise error
        return gpu_info
