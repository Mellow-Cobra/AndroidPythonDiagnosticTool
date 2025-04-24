# Local Imports
import logging
from hardware_probes.battery import AdbBatteryProbe

# Third Part Imports


logger = logging.getLogger(__name__)


class AndroidBatteryDiagnostics:
    """Class used to run Android Battery Diagnostics"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_battery_probe = AdbBatteryProbe(device_serial_number=device_serial_number)

    def level_zero_battery_diagnostics(self):
        """Method used to run Level zero battery diagnostics"""
        self._adb_battery_probe.get_battery_level()
        self._adb_battery_probe.get_battery_technology()
        self._adb_battery_probe.get_battery_health()
        self._adb_battery_probe.get_battery_voltage()
        self._adb_battery_probe.get_battery_temperature()

    def level_one_battery_diagnostics(self):
        """Method used to collect level one battery diagnostics"""
        self._adb_battery_probe.monitor_battery_temperature()
