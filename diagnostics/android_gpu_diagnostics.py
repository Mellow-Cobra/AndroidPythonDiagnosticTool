# Standard Imports

import logging

# Local Imports
from builders.gpu.gpu_factory import GpuFactory

logger = logging.getLogger(__name__)


class AndroidGPUDiagnostics:
    """GPU diagnostics class"""

    def __init__(self, device_serial_number, configuration):
        """Constructor"""
        self._adb_gpu_interface = GpuFactory.detect_gpu(serial_number=device_serial_number)
        self.device_serial_number = device_serial_number
        self.configuration = configuration

    def gpu_level_zero_diagnostics(self):
        """GPU level one diagnostics"""
        temp = self._adb_gpu_interface.get_gpu_temperature()
        frequency = self._adb_gpu_interface.get_gpu_frequency()
        logger.info(temp)
        logger.info(frequency)

    def gpu_level_one_diagnostics(self):
        """GPU level two diagnostics"""
        pass

    def capture_gpu_baseline(self):
        """Method used to capture GPU baseline"""

