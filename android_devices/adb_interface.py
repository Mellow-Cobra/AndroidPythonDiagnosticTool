import glob
import logging
import subprocess
import re

# Local Imports
from constants import *

logger = logging.getLogger(__name__)

class AdbInterface:
    """Class used to interface with Android Device over ADB"""


    def __init__(self, device_serial_number=None, host="8.8.8.8"):
        """Constructor"""
        self.device_serial_number = device_serial_number
        self.pingable_host = host

    def run_adb_command(self, cmds):
        """Method used to open adb shell"""
        cmds_split = cmds.split(" ")
        base_cmd = ['adb', '-s']

        if self.device_serial_number:
            base_cmd.append(self.device_serial_number)
        else:
            try:
                logger.info("Serial number not provided will defualt to first adb device")
                base_cmd = ['adb', 'devices']
                adb_default_device = subprocess.run(base_cmd, capture_output=True)
                adb_devices_output = adb_default_device.stdout.decode("utf-8").strip().split("\n")[1:]
                for line in adb_devices_output:
                    if DEVICE in line and not line.startswith("*"):
                        self.device_serial_number = line.split()[0]
                        base_cmd.append('-s')
                        base_cmd.append(self.device_serial_number)
            except (ConnectionError, IOError):
                logger.info("Could not connect to any Android device")
                exit(1)
        base_cmd.append('shell')
        for cmd in cmds_split:
            base_cmd.append(cmd)

        try:
            output = subprocess.run(base_cmd, capture_output=True)
            print(output)
            if output.returncode == 0:
                return output.stdout.decode("utf-8").strip()
            else:
                raise RuntimeError(f"Could not run ADB command. Error {output.stderr.strip()}")
        except Exception as exception:
            logger.info(f"Encountered: {exception}")




        raw_cmd_output = subprocess.run(base_cmd, stdout=subprocess.PIPE,
                                    capture_output=True)
        cmd_output = raw_cmd_output.stdout.decode("utf-8").strip()

        return cmd_output

    def get_available_devices(self, ):
        """Method used to get available devices
          ::return - list of devices and default device """
        logger.info("Finding all Android devices connected to PC")
        devices = list()
        try:
            adb_devices = subprocess.run(["adb", "devices"], capture_output=True)
            adb_devices_attached_to_system = adb_devices.stdout.decode("utf-8").split("\n")[1:]
            for dev in adb_devices_attached_to_system:
                devices.append(dev)
            self.device_serial_number = devices[0]
            return devices, self.device_serial_number
        except Exception as error:
            logger.info(f"Exception Caught: {error}")
            logger.info("Try restarting Android Device, Installing ADB Drivers,"
                        "Checking system environment variables, or reconnecting the USB cable.")
            raise RuntimeError

    






