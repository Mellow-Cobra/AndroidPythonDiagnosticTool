# Standard Imports
import logging


# Local Imports
from hardware_probes.cpu import AdbCpuProbe

logger = logging.getLogger(__name__)

class CpuMonitor:
    """Class used to monitor CPU on an Android device"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_cpu_probe = AdbCpuProbe(device_serial_number)

    def monitor_cpu_temperature(self):
        """Method used to monitor cpu temperature"""
        cpu_temperatures = self._adb_cpu_probe.get_cpu_temperatures()
        cpus = cpu_temperatures.get("CPU", [])
        temperatures_values = cpu_temperatures.get("Temperature", [])

        return cpus, temperatures_values
