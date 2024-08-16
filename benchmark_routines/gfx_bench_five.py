import subprocess

from pandas.core.dtypes.generic import ABCDatetimeArray

# Local Imports
import constants



class GFXBench:
    """Class method used to run GFX Bench Routines"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        self.serial_number = serial_number
        self.configuration = configuration

    def launch_gfx_bench(self):
        """Method used to launch GFX Bench"""
        subprocess.run(["adb", "shell", "am", "start",
                        "-n", "net.kishonti.gfxbench.vulkan.v50000.corporate/net.kishonti.benchui.BenchTestActivity"])

    def run_trex_benchmark(self):
        """Method used to run trex benchmark"""
        trex_on_screen_out = subprocess.run(["adb", "-s", f"{self.serial_number}", "shell", "am",
                        "broadcast", "-a", "net.kishonti.testfw.ACTION_RUN_TESTS",
                        "-n net.kishonti.gfxbench.vulkan.v50000.corporate/net.kishonti.benchui.corporate.CommandLineSession",
                        "-e", "test_ids gl_trex"], capture_output=True)
        trex_on_screen_out = trex_on_screen_out.stdout.decode("utf-8")

        print(trex_on_screen_out)

