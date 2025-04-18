import os.path
import json
import datetime

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import platform
import logging.config
import sys

from yaml import serialize

# Local Imports
from android_devices.adb_interface import AdbInterface
from diagnostics.android_cpu_diagnostics import AndroidCpuDiagnostics
from diagnostics.android_wifi_diagnostics import WifiDiagnostics
from diagnostics.android_gpu_diagnostics import AndroidGPUDiagnostics
from benchmark_routines.gfx_bench_five import GFXBench
from constants import *


time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

log_name = f"C:\\Users\\inter\\OneDrive\\Documents\\Results\\logs\\adt_log_{time_stamp}.log"

if platform.system() == LINUX:
    if not os.path.exists('/tmp/android_logs'):
        os.makedirs('/tmp/android_logs')
elif platform.system() == WIN:
    if not os.path.exists('C:\\Users\\inter\\OneDrive\\Documents\\Results\\logs\\'):
        os.makedirs('C:\\Users\\inter\\OneDrive\\Documents\\Results\\logs')
logging.basicConfig(filename=log_name, level=logging.INFO)


# logging.config.fileConfig('C:\\Users\\inter\\OneDrive\\Documents\\Results\\logs\\adt_log.log')

class BatteryDiagnostics(QThread):
    """Class used to run battery diagnostics"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        super().__init__()
        self.serial_number = serial_number
        self.configuration = configuration

    def run(self):
        """Thread runner method for battery diagnostics"""
        battery_diag = AdbInterface(serial_number=self.serial_number)
        battery_diag.get_battery_level()

class RunTrexOnScreen(QThread):
    """Class used to run Trex On Screen"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        super().__init__()
        self.serial_number = serial_number
        self.configuration = configuration

    def run(self):
        """Thread runner method for T-Rex on screen"""
        gfx_bench_five = GFXBench(serial_number=self.serial_number, configuration=self.configuration)
        gfx_bench_five.launch_gfx_bench()
        gfx_bench_five.run_trex_benchmark()


class RunAndroidDiagnostics(QThread):
    """Thread class used to run cpu diagnostics"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        super().__init__()
        self.serial_number = serial_number
        self.configuration = configuration

    def run(self):
        """Thread runner method"""
        android_cpu_diagnostics = AndroidCpuDiagnostics(self.serial_number, self.configuration)
        android_cpu_diagnostics.run_cpu_diagnostics()
        # android_wifi_diagnostics = WifiDiagnostics(self.serial_number, self.configuration)
        # android_wifi_diagnostics.run_wifi_diagnostics()

class RunAndroidGPUDiagnostics(QThread):
    """Thread class used to android gpu diagnostics"""

    def __init__(self, serial_number, configuration):
        """Constructor"""
        super().__init__()
        self.serial_number = serial_number
        self.configuration = configuration

    def run(self):
        """Thread runner method"""
        android_gpu_diagnostics = AndroidGPUDiagnostics(device_serial_number=self.serial_number,
                                                        configuration=self.configuration)
        android_gpu_diagnostics.gpu_level_zero_diagnostics()




class GeekBenchFive(QThread):
    """Class used to run  GeekBench Bench mark"""

    def __init__(self):
        """Constructor"""

    def run(self):
        """Thread runner method for Geek Bench 5 diagnostics"""


class AndroidDiagFrontPanel(QWidget):
    """GUI Class for Android Diagnostic Panel"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android Diagnostic Tool")
        self.setFixedSize(1024, 768)
        self.main_layout = QVBoxLayout()
        self.serial_numbers = None
        self.config_file = None

        # Create Tabs
        tabs = QTabWidget()
        self.diagnostic_tab = QWidget()
        self.configuration_tab = QWidget()
        self.benchmark_tab = QWidget()
        tabs.addTab(self.diagnostic_tab, "Diagnostics Tab")
        tabs.addTab(self.benchmark_tab, "Benchmark Tab")
        tabs.addTab(self.configuration_tab, "Configuration Tab")

        # Diagnostic Tab Layout
        self.diagnostic_tab.layout = QGridLayout()
        self.diagnostic_tab_sub_layout_one = QVBoxLayout()
        self.diagnostic_tab_sub_layout_two = QVBoxLayout()
        self.diagnostic_tab_sub_layout_three = QVBoxLayout()
        self.get_imei_number_button = QPushButton("Get IMEI Number")
        self.battery_diagnostics_button = QPushButton("Battery Diagnostics")
        self.disable_wifi_radio_button = QPushButton("Disable Wifi")
        self.enable_wifi_radio_button = QPushButton("Enable Wifi")
        self.enable_nfc_button = QPushButton("Enable NFC")
        self.disable_nfc_button = QPushButton("Disable NFC")
        self.super_user_mode_button = QPushButton("Super User Mode")
        self.gpu_diagnostics_button = QPushButton("Run GPU Diagnostics")
        self.run_android_diagnostics_button = QPushButton("Run Android Diagnostics")
        self.diagnostic_text_box = QTextEdit()
        self.diagnostic_tab_sub_layout_one.addWidget(self.get_imei_number_button)
        self.diagnostic_tab_sub_layout_one.addWidget(self.disable_wifi_radio_button)
        self.diagnostic_tab_sub_layout_one.addWidget(self.enable_wifi_radio_button)
        self.diagnostic_tab_sub_layout_one.addWidget(self.enable_nfc_button)
        self.diagnostic_tab_sub_layout_one.addWidget(self.disable_nfc_button)
        self.diagnostic_tab_sub_layout_one.addWidget(self.super_user_mode_button)
        self.diagnostic_tab_sub_layout_two.addWidget(self.battery_diagnostics_button)
        self.diagnostic_tab_sub_layout_two.addWidget(self.gpu_diagnostics_button)
        self.diagnostic_tab_sub_layout_two.addWidget(self.run_android_diagnostics_button)
        #self.diagnostic_tab_sub_layout_three.addWidget(self.diagnostic_text_box)
        self.diagnostic_tab.layout.addLayout(self.diagnostic_tab_sub_layout_one, 0, 0)
        self.diagnostic_tab.layout.addLayout(self.diagnostic_tab_sub_layout_two, 0, 1)
        self.diagnostic_tab.setLayout(self.diagnostic_tab.layout)

        # Diagnostic Button Connections
        self.enable_wifi_radio_button.clicked.connect(self.on_enable_wifi)
        self.run_android_diagnostics_button.clicked.connect(self.on_run_android_diagnostics)
        self.gpu_diagnostics_button.clicked.connect(self.on_run_gpu_diagnostics)

        # Benchmark Tab Layout
        self.benchmark_tab.layout = QGridLayout()
        self.bench_mark_tab_sub_layout_gfx = QHBoxLayout()
        self.run_trex_bench_mark_button = QPushButton("Run Trex On Screen")
        self.run_egypt_bench_mark_button = QPushButton("Run Egypt")
        self.run_geekbench_five = QPushButton("GeekBench 5")
        self.run_trex_bench_mark_button.clicked.connect(self.run_trex_on_screen)
        self.bench_mark_tab_sub_layout_gfx.addWidget(self.run_trex_bench_mark_button)
        self.bench_mark_tab_sub_layout_gfx.addWidget(self.run_egypt_bench_mark_button)
        self.bench_mark_tab_sub_layout_gfx.addWidget(self.run_trex_bench_mark_button)
        self.benchmark_tab.layout.addLayout(self.bench_mark_tab_sub_layout_gfx, 0, 0)
        self.benchmark_tab.setLayout(self.benchmark_tab.layout)

        # Configuration Tab Layout
        self.configuration_tab.layout = QGridLayout()
        self.configuration_tab_sub_layout_one = QVBoxLayout()
        self.configuration_tab_sub_layout_two = QVBoxLayout()
        self.configuration_tab_sub_layout_three = QGridLayout()
        self.android_phone_serial_number_label = QLabel("Devices to Test Serial Numbers")
        self.android_phone_serial_number = QLineEdit("Separate by comma")
        self.android_diagnostics_configuration_label = QLabel("Configuration File Path")
        self.android_diagnostics_configuration = QLineEdit("Configuration File Path")
        self.get_android_device_serial_number_button = QPushButton("Get Available Devices")
        self.load_configuration_file_button = QPushButton("Load Config")
        self.android_serial_number_text_box = QTextEdit("Available Device Serial Numbers")
        self.configuration_tab_sub_layout_two.addWidget(self.get_android_device_serial_number_button)
        self.configuration_tab_sub_layout_two.addWidget(self.android_serial_number_text_box)
        self.get_android_device_serial_number_button.clicked.connect(self.get_available_devices_serial_numbers)
        self.load_configuration_file_button.clicked.connect(self.load_configuration_file)
        self.configuration_tab_sub_layout_three.addWidget(self.android_diagnostics_configuration_label, 0, 0)
        self.configuration_tab_sub_layout_three.addWidget(self.android_diagnostics_configuration, 0, 1)
        self.configuration_tab_sub_layout_three.addWidget(self.load_configuration_file_button, 1, 0, 1, 2)
        self.configuration_tab_sub_layout_three.addWidget(self.android_phone_serial_number_label, 2, 0)
        self.configuration_tab_sub_layout_three.addWidget(self.android_phone_serial_number, 2, 1)
        self.configuration_tab_sub_layout_one.addLayout(self.configuration_tab_sub_layout_three)
        self.configuration_tab.layout.addLayout(self.configuration_tab_sub_layout_one, 0, 0)
        self.configuration_tab.layout.addLayout(self.configuration_tab_sub_layout_two, 0, 1)
        self.configuration_tab.setLayout(self.configuration_tab.layout)

        # Event listeners for diagnostics tab
        self.battery_diagnostics_button.clicked.connect(self.on_run_battery_diagnostics)

        self.main_layout.addWidget(tabs)
        self.setLayout(self.main_layout)

        self.show()

    def on_run_battery_diagnostics(self):
        """Event handler for battery diagnostics"""
        for _, device_serial in enumerate(self.serial_numbers):
            battery_diagnostics = BatteryDiagnostics(serial_number=self.serial_numbers,
                                                     configuration=self.config_file)
            battery_diagnostics.run()

    def run_geekbench_five(self):
        """Event handler used to GeekBench 5"""
        geek_bench_thread = GeekBenchFive()

    def on_enable_wifi(self):
        """Event handler for enabling WiFi"""

    def on_run_gpu_diagnostics(self):
        """Method used to run GPU Diagnostics"""
        for _ , device_serial in enumerate(self.serial_numbers):
            android_gpu_diagnostics_thread = RunAndroidGPUDiagnostics(serial_number=device_serial,
                                                                      configuration=self.config_file)
            android_gpu_diagnostics_thread.run()


    def get_available_devices_serial_numbers(self):
        """Event handler for finding serial numbers"""
        abd_interface = AdbInterface()
        device_serial_numbers, default_serial_number = abd_interface.get_available_devices()
        self.android_serial_number_text_box.clear()
        for _, serial_number in enumerate(device_serial_numbers):
            self.android_serial_number_text_box.append(serial_number)


    def on_run_android_diagnostics(self):
        """Method used to spawn threads and test devices"""
        for _, device_serial in enumerate(self.serial_numbers):
            android_diagnostics_thread = RunAndroidDiagnostics(serial_number=device_serial,
                                                               configuration=self.config_file)
            android_diagnostics_thread.run()

    def run_trex_on_screen(self):
        """Method used to run T-Rex on screen"""
        for _, device_serial in enumerate(self.serial_numbers):
            android_trex_thread = RunTrexOnScreen(serial_number=device_serial, configuration=self.config_file)
            android_trex_thread.run()

    def load_configuration_file(self):
        """Method used to load configuration file"""
        config_file_path = str(r"C:\Users\inter\PycharmProject\AndroidPythonDiagnosticTool\configuration\android_diag_config.json")
        #self.android_diagnostics_configuration.text())
        with open(config_file_path, mode='r', encoding='utf-8') as config_file:
            self.config_file = json.load(config_file)
        self.serial_numbers = self.config_file[ANDROID_SETTINGS][ANDROID_DEVICES]



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AndroidDiagFrontPanel()
    sys.exit(app.exec())
