from android_devices.adb_interface import AdbInterface
import logging


logger = logging.getLogger(__name__)


class WifiProbe:
    """Class containg ADB shell low level WiFi probes"""

    def __init__(self, device_serial_number, host="8.8.8.8"):
        """Constructor"""
        self.adb_shell = AdbInterface(device_serial_number)
        self.host = host

    def get_wifi_radio_status(self):
        """Method used to get status of WiFi from Android device"""
        logger.info("Retrieving WiFi status")
        wifi_status = subprocess.run(['adb', '-s', f'{self.serial_number}', 'shell', 'dumpsys wifi', ' | grep "Wi-Fi is"'],
                                     capture_output=True)

        wifi_status = wifi_status.stdout.decode("utf-8").split(" ")

        return wifi_status[2].strip("\n")


    def get_wifi_network_info(self):
        """Method used to get Wi-Fi network information"""
        logger.info("Retrieving WiFi network information")

        wifi_net_info = subprocess.run(['adb', '-s', f'{self.serial_number}', 'shell', 'dumpsys wifi','| grep  mNetworkInfo'], capture_output=True)

        wifi_net_info = wifi_net_info.stdout.decode('utf-8').splitlines()

        return wifi_net_info[0].split(" ")[4].strip(',')


    def get_wifi_internet_status(self):
        """Method used to determine if android device can connect to internet over wifi"""
        wifi_internet_info, _ = adb_shell.communicate(b'dumpsys connectivity')
        print(wifi_internet_info)

    def get_global_wifi_settings(self):
        """Method used to determine global wifi settings"""
        adb_shell = self.open_adb_shell()
        wifi_global_status, _ = adb_shell.communicate(b'settings get global wifi_on')
        print(wifi_global_status)

    def run_ping_test(self):
        adb_shell = self.open_adb_shell()
        ping_test_command = bytes(f'ping -c 4 {self.pingable_host}', 'utf-8')
        ping_test_result, _ = adb_shell.communicate(ping_test_command)

        print(ping_test_result)

    def run_link_probe(self):
        """Method used to run link probe"""
        adb_shell = self.open_adb_shell()
        link_probe_result, _ = adb_shell.communicate(b'cmd wifi send-link-probe')
        print(link_probe_result)

    def disconnect_from_wifi_network(self):
        """Method used to diconnect from Wi-Fi"""
        adb_shell = self.open_adb_shell()
        disconnect_status, _ = adb_shell.communicate(b'cmd wifi')

    def disable_wifi_scanning(self):
        """Method used to disable Wi-Fi scanning"""
        adb_shell = self.open_adb_shell()
        wifi_scanning_status, _ = adb_shell.communicate(b'settings put global wifi_on 0')

        print(wifi_scanning_status)

    def set_global_wifi_off(self):
        """Method used to set global wifi to off"""
        adb_shell = self.open_adb_shell()
        wifi_global_status, _ = adb_shell.communicate(b'settings put global wifi_on 0')

        print(wifi_global_status)

    def set_global_wifi_on(self):
        """Method used to set global wifi to on"""
        adb_shell = self.open_adb_shell()
        wifi_global_status, _ = adb_shell.communicate(b'settings put global wifi_on 1')

        print(wifi_global_status)

    def get_wifi_station_ssid(self):
        """Get Wi-Fi service set indentifier"""
        adb_shell = self.open_adb_shell()
        wifi_ssid = subprocess.run(["adb", "-s", f"{self.serial_number}", "shell", "iw wlan0 info | grep ssid"],
                                   capture_output=True)

        wifi_ssid = wifi_ssid.stdout.decode("utf-8").split(" ")

        return wifi_ssid[1]

    def get_signal_strength(self):
        """Get Wi-Fi singal strength"""
        adb_shell = self.open_adb_shell()
        wifi_signal_strength = subprocess.run(["adb", "-s", f"{self.serial_number}", "shell",
                                                    "iw dev wlan0 link | grep signal"], capture_output=True)

        wifi_signal_strength = wifi_signal_strength.stdout.decode("utf-8")

        wifi_signal_regex = r"\s\-([0-9])*\s\bdBm\b"

        match = re.search(pattern=wifi_signal_regex, string=wifi_signal_strength)
        if match:
            wifi_signal_strength = match.group()
        else:
            wifi_signal_strength = NOT_AVAILABLE

        return wifi_signal_strength

    def disconnect_from_wifi(self):
        """Method used to disconnect from wifi"""
        adb_shell = self.open_adb_shell()
        disconnect_wifi, _ = adb_shell.communicate(b'iw dev wlan0 disconnect')
    def enable_airplane_mode(self):
        """Method used to enable airplane mode"""
        adb_shell = self.open_adb_shell()
        airplane_mode_status, _ = adb_shell.commmunicate(b'settings put global airplane_mode_on 1')