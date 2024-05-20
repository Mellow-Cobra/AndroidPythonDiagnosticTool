from PyQt6.QtWidgets import *
from PyQt6.QtCore import  *
import sys

# Local Imports
from android_devices.adb_interface import AdbInterface


class BatteryDiagnostics(QThread):
    """Class used to run battery diagnostics"""

    def __init__(self):
        """Constructor"""
        # self.serial_number = serial_number

    def run(self):
        """Thread runner method for battery diagnostics"""
        battery_diag = AdbInterface()
        battery_diag.get_battery_level()
class AndroidDiagFrontPanel(QWidget):
    """GUI Class for Android Diagnostic Panel"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Android Diagnostic Tool")
        self.setFixedSize(1024, 768)
        self.main_layout = QVBoxLayout()

        # Create Tabs
        tabs = QTabWidget()
        self.diagnostic_tab = QWidget()
        self.configuration_tab = QWidget()
        tabs.addTab(self.diagnostic_tab, "Diagnostics Tab")
        tabs.addTab(self.configuration_tab, "Configuration Tab")


        # Diagnostic Tab Layout
        self.diagnostic_tab.layout = QGridLayout()
        self.diagnostic_tab.setLayout(self.diagnostic_tab.layout)
        self.diagnostic_tab_sub_layout = QVBoxLayout()
        self.battery_diagnostics_button = QPushButton("Battery Diagnostics")
        self.disable_wifi_radio_button = QPushButton("Disiable Wifi")
        self.enable_wifi_radio_button = QPushButton("Enable Wifi")
        self.enable_nfc_button = QPushButton("Enable NFC")
        self.disable_nfc_button = QPushButton("Disable NFC")
        self.super_user_mode_button = QPushButton("Super User Mode")
        self.diagnostic_text_box = QTextEdit()
        self.diagnostic_tab_sub_layout.addWidget(self.battery_diagnostics_button)
        self.diagnostic_tab_sub_layout.addWidget(self.disable_wifi_radio_button)
        self.diagnostic_tab_sub_layout.addWidget(self.enable_wifi_radio_button)
        self.diagnostic_tab_sub_layout.addWidget(self.enable_nfc_button)
        self.diagnostic_tab_sub_layout.addWidget(self.disable_nfc_button)
        self.diagnostic_tab_sub_layout.addWidget(self.super_user_mode_button)
        self.diagnostic_tab_sub_layout.addWidget(self.diagnostic_text_box)
        self.diagnostic_tab.layout.addLayout(self.diagnostic_tab_sub_layout, 0, 0)
        self.diagnostic_tab.setLayout(self.diagnostic_tab.layout)

        # Diagnostic Button Connections
        self.enable_wifi_radio_button.clicked.connect(self.on_enable_wifi)


        # Configuration Tab Layout
        self.configuration_tab.layout = QGridLayout()
        self.android_phone_serial_number_label = QLabel("Serial Number")
        self.android_phone_serial_number = QLineEdit("Enter Android Phone Serial")
        self.configuration_tab.layout.addWidget(self.android_phone_serial_number_label, 0, 0)
        self.configuration_tab.layout.addWidget(self.android_phone_serial_number, 0, 1)
        self.configuration_tab.setLayout(self.configuration_tab.layout)

        # Event listeners for diagnostics tab
        self.battery_diagnostics_button.clicked.connect(self.on_run_battery_diagnostics)
        


        self.main_layout.addWidget(tabs)
        self.setLayout(self.main_layout)

        self.show()

    def on_run_battery_diagnostics(self):
        """Event handler for battery diagnostics"""
        battery_diagnostics = BatteryDiagnostics()
        battery_diagnostics.run()

    def on_enable_wifi(self):
        """Event handler for enabling WiFi"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AndroidDiagFrontPanel()
    sys.exit(app.exec())