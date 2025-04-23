# Standard Imports
import logging
import re



# Local Imports
from android_devices.adb_interface import AdbInterface
from constants import *


logger = logging.getLogger(__name__)

class AdbBatteryProbe:
    """Class used to probe battery over ADB"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_shell = AdbInterface(device_serial_number)


    def get_battery_level(self):
        """Method used to pull battery diagnostics from android phone"""
        battery_level = self._adb_shell.run_adb_command("dumpsys battery | grep level")
        battery_level_regex = r"\blevel\b:\s\d*"
        match = re.search(pattern=battery_level_regex, string=battery_level)
        battery_level = dict()
        if match:
            match_stripped = match.group().strip("level: ")
            logger.info(f"Battery Level: {match_stripped}%")
            battery_level.update({"Battery level": f"{match_stripped}%"})
            return battery_level
        else:
            logger.info(f"Could not determine battery level reading: {NOT_AVAILABLE}")
            return NOT_AVAILABLE
