

# Local Imports
from android_devices.adb_interface import AdbInterface


class GeekBenchFive:

    def __init__(self, serial_number):
        """Constructor"""
        self.abd_interface = AdbInterface(serial_number)


    def run_geek_bench_five(self):
        """Method used to run Geek Bench Five"""
