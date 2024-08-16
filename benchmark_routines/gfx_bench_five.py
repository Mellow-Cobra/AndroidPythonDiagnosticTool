import subprocess

from pandas.core.dtypes.generic import ABCDatetimeArray

# Local Imports

class GFXBench:
    """Class method used to run GFX Bench Routines"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        self.serial_number = serial_number
        self.configuration = configuration

    def run_trex_benchmark(self):
        """Method used to run trex benchmark"""
        subprocess.run(["adb", "-s", f"{self.serial_number}", "shell am  broadcast",
                        ' -a net.kishonti.testfw.ACTION_RUN_TESTS -n ',
                        'net.kishonti.gfxbench.vulkan.v50000.corporate/',
                        'net.kishonti.benchui.corporate.CommandLineSession -e test_ids gl_trex'])
