# Standard Imports
import logging
import re

# Local Imports
from android_devices.adb_interface import AdbInterface

logger = logging.getLogger(__name__)


class AdbController:
    """A class used to turn off system features such as NFC, WiFi, and Bluetooth"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_shell = AdbInterface(device_serial_number)


    def enable_super_user_mode(self):
        """Method used to enable super-user mode"""
        logger.info("Enabling super user mode")
        super_user_mode = self._adb_shell.run_adb_command("root")
        logger.info(super_user_mode)


    def disable_wifi_service(self):
        """Method used to disable WiFi radio"""
        logger.info("Disabling WiFi service")
        disabled_wifi = self._adb_shell.run_adb_command("svc wifi disable")


        return disabled_wifi


    def enable_wifi_service(self):
        """Method used to enable WiFi radio"""
        logger.info("Enabling WiFi Service")
        enabled_wifi = self._adb_shell.run_adb_command("svc wifi enable")



        return enabled_wifi


    def enable_nfc_service(self):
        """Method used to enable NFC radio"""
        logger.info("Enabling NFC service")
        enabled_nfc = self._adb_shell.run_adb_command("svc nfc enable")



        return enabled_nfc
