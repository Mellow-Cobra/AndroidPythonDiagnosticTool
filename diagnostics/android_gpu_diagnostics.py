# Standard Imports

import logging

# Local Imports
from hardware_probes.gpu import AdbGpuProbe

logger = logging.getLogger(__name__)


class AndroidGPUDiagnostics:
    """GPU diagnostics class"""

    def __init__(self, device_serial_number, configuration):
        """Constructor"""
        self._adb_gpu_interface = AdbGpuProbe(device_serial_number)
        self.device_serial_number = device_serial_number
        self.configuration = configuration

    def gpu_level_zero_diagnostics(self):
        """GPU level one diagnostics"""
        gpu = self._adb_gpu_interface.get_gpu_information()
        print(gpu)

    def gpu_level_one_diagnostics(self):
        """GPU level two diagnostics"""
        pass

