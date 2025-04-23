# Local Imports
import csv
import datetime
import os
import logging
from hardware_probes.battery import AdbBatteryProbe
from device_control.android_system_control import AdbController
from constants import *

# Third Part Imports
import pandas as pd
from jinja2 import Template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


logger = logging.getLogger(__name__)


class AndroidBatteryDiagnostics:
    """Class used to run Android Battery Diagnostics"""

    def __init__(self, device_serial_number):
        """Constructor"""
        self._adb_battery_probe = AdbBatteryProbe(device_serial_number=device_serial_number)

    def level_zero_battery_diagnostics(self):
        """Method used to run Level zero battery diagnostics"""
        self._adb_battery_probe.get_battery_level()
