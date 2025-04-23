# Standard Imports
import logging
import re



# Local Imports
from android_devices.adb_interface import AdbInterface
from core.constants import *
from core.enums import BatteryHealth


logger = logging.getLogger(__name__)

class AdbBatteryProbe:
    """Class used to probe battery over ADB"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_shell = AdbInterface(device_serial_number)

    def battery_adb_dumpsys(self, match_string):
        """Method used for repeated command calls of adb shell dumpsys battery"""
        batt_dumpsys_output = self._adb_shell.run_adb_command(f"dumpsys battery | grep {match_string}")

        return batt_dumpsys_output


    def get_battery_level(self):
        """Method used to pull battery diagnostics from android phone"""
        adb_output = self.battery_adb_dumpsys("level")
        battery_level_regex = r"\blevel\b:\s\d*"
        match = re.search(pattern=battery_level_regex, string=adb_output)
        battery_level = dict()
        if match:
            match_stripped = match.group().strip("level: ")
            logger.info(f"Battery Level: {match_stripped}%")
            battery_level.update({"Battery level": f"{match_stripped}%"})
            return battery_level
        else:
            logger.info(f"Could not determine battery level reading: {NOT_AVAILABLE}")
            return NOT_AVAILABLE


    def get_battery_technology(self):
        """Method used to status of battery charging"""
        adb_output = self.battery_adb_dumpsys("technology")
        battery_technology_regex = r"technology:\s[A-Za-z0-9\s\-\_\@\#\!\.\$\,]+"
        match = re.search(pattern=battery_technology_regex, string=adb_output)
        battery_technology = dict()
        if match:
            match_stripped = match.group().lstrip("technology:")
            logger.info(f"Battery Technology: {match_stripped}")
            battery_technology.update({"Battery Technology": f"{match_stripped}"})
            return battery_technology
        else:
            logger.info(f"Could not determine battery technology: {NOT_AVAILABLE}")
            return NOT_AVAILABLE

    def get_battery_health(self):
        """Method used to determine battery voltage"""
        adb_output = self.battery_adb_dumpsys("health")
        battery_health_regex = r"health:\s[0-7]"
        match = re.search(pattern=battery_health_regex, string=adb_output)
        battery_health = dict()
        if match:
            match_stripped = match.group().lstrip("heatlh:")
            battery_health.update({"Battery Health": f"{BatteryHealth(int(match_stripped)).name}"})
            logger.info(battery_health)
            return battery_health
        else:
            logger.info("Could not determine battery health")
            battery_health.update({"Battery Health": NOT_AVAILABLE})
            return battery_health



