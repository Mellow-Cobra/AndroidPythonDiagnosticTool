import glob
import logging
import subprocess
import re

# Local Imports
from constants import *

logger = logging.getLogger(__name__)

class AdbInterface:
    """Class used to interface with Android Device over ADB"""


    def __init__(self, serial_number=None, host="8.8.8.8"):
        """Constructor"""
        self.serial_number = serial_number
        self.pingable_host = host

    def open_adb_shell(self):
        """Method used to open adb shell"""

        adb_proc = subprocess.Popen(['adb', '-s', f'{self.serial_number}', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    shell=False)

        return adb_proc

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

    def get_battery_level(self):
        """Method used to pull battery diagnostics from android phone"""
        battery_level = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                "shell", "dumpsys", "battery", "| grep level"], capture_output=True)
        battery_level = battery_level.stdout.decode("utf-8")
        battery_level_regex = r"\blevel\b:\s\d*"
        match = re.search(pattern=battery_level_regex, string=battery_level)
        if match:
            print(match.group())
        else:
            return NOT_AVAILABLE

        return battery_level

    def enable_super_user_mode(self):
        """Method used to enable super user mode"""
        logger.info("Enabling super user mode")
        super_user_mode = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                          "root"], capture_output=True)
        super_user_mode.stdout.decode("utf-8")

    def disable_wifi_service(self):
        """Method used to disable WiFi radio"""
        logger.info("Disabling WiFi service")
        disabled_wifi = subprocess.run(["adb", "shell", "svc wifi disable"], capture_output=True)

        disabled_wifi = disabled_wifi.stdout.decode("utf-8")

        return disabled_wifi

    def enable_wifi_service(self):
        """Method used to enable WiFi radio"""
        logger.info("Enabling WiFi Service")
        enabled_wifi = subprocess.run(["adb", "shell", "svc wifi enable"], capture_output=True)

        enabled_wifi = enabled_wifi.stdout.decode("utf-8")

        return enabled_wifi

    def enable_nfc_service(self):
        """Method used to enable NFC radio"""
        logger.info("Enabling NFC service")
        enabled_nfc = subprocess.run(["adb", "shell", "svc nfc enable"])

        enabled_nfc = enabled_nfc.stdout.decode("utf-8")

        return enabled_nfc

    def get_cpu_temperatures(self):
        """Method used to get CPU temperatures"""
        logger.info("Retrieving CPU temperatures")
        temperatures = list()
        thermal_service = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                          "shell", "dumpsys thermalservice", " | grep CPU"], capture_output=True)

        thermal_service = thermal_service.stdout.decode("utf-8").splitlines()
        del thermal_service[:8]

        temp_regex = r"\bmValue\b=([0-9])*\.([0-9])*"
        for _, temp in enumerate(thermal_service):

            match = re.search(pattern=temp_regex, string=temp)
            if match:
                temperatures.append(float(match.group().strip("mValue=")))

        return temperatures

    def get_cpu_frequencies(self):
        """Method used to get CPU frequencies"""
        logger.info("Retrieving current CPU frequencies")
        cpu_frequencies = list()
        available_cpus = subprocess.run(["adb", "-s", f"{self.serial_number}", "shell",
                                         "find", "/sys/devices/system/cpu/", "-name", "cpu[0-9]*"],
                                        capture_output=True)

        available_cpus = sorted(available_cpus.stdout.decode("utf-8").splitlines())

        for index, cpu_directory in enumerate(available_cpus):
            cpu_freq = subprocess.run([f"adb", "-s",  f"{self.serial_number}",
                                       "shell", f"cat {cpu_directory}/cpufreq/cpuinfo_cur_freq"],
                           capture_output=True)
            cpu_freq = float(cpu_freq.stdout.decode("utf-8").strip('\r\n'))
            cpu_frequencies.append(cpu_freq)

        return cpu_frequencies

    def get_cpu_max_speed(self):
        """Method used to get cpu max speed"""
        logger.info("Capturing CPU maximum speed...")
        cpu_max_speeds = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                        "shell", "cat", "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_max_freq"],
                                       capture_output=True)
        cpu_max_speeds = cpu_max_speeds.stdout.decode("utf-8").splitlines()

        return cpu_max_speeds

    def get_cpu_min_speed(self):
        """Method used to get cpu min speed"""
        logger.info("Capturing minimum CPU speeds...")
        cpu_min_speeds = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                         "shell", "cat", "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_min_freq"],
                                        capture_output=True )
        cpu_min_speeds = cpu_min_speeds.stdout.decode("utf-8").splitlines()

        return cpu_min_speeds
    def get_available_devices(self):
        """Method used to get available devices"""
        logger.info("Finding all Android devices connected to PC")
        try:
            adb_devices = subprocess.run(["adb", "devices"], capture_output=True)
            adb_devices = adb_devices.stdout.decode("utf-8").splitlines()
        except FileNotFoundError as error:
            logger.info(error)
            logger.info('Install ADB Drivers')
        del adb_devices[0]
        del adb_devices[-1]
        serial_numbers = list()
        regex_to_remove =  r"\t.*"
        for i in range(len(adb_devices)):
            match = re.findall(pattern=regex_to_remove, string=adb_devices[i])
            if match:
                serial_numbers.append(adb_devices[i].strip(match[0]))


        return serial_numbers

    def get_gpu_model(self):
        """Method used to get GPU model"""
        logger.info("Capturing GPU model information...")
        gpu_model_information = subprocess.run(["adb", "-s", f"{self.serial_number}", "shell", "dumpsys",
                        "SurfaceFlinger", "|", "grep", "GLES"], capture_output=True)
        gpu_model_information = gpu_model_information.stdout.decode("utf-8")

        return gpu_model_information




if __name__ == "__main__":
    adb = AdbInterface()
    adb.get_cpu_temperatures()