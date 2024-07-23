import glob
import subprocess
import re

# Local Imports
from constants import *

class AdbInterface:
    """Class used to interface with Android Device over ADB"""


    def __init__(self, serial_number):
        """Constructor"""
        self.adb_shell = self.open_adb_shell(serial_number)

    def open_adb_shell(self, serial_number):
        """Method used to open adb shell"""
        adb_proc = subprocess.Popen(['adb', '-s', f'{serial_number}', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    shell=False)

        return adb_proc

    def get_wifi_status(self):
        """Method used to get status of WiFi from Android device"""
        wifi_status, _ = self.adb_shell.communicate(b'dumpsys wifi | grep "Wi-Fi is"')


        print(wifi_status.decode('utf-8'))


    def get_wifi_network_info(self):
        """Method used to get Wi-Fi network information"""
        wifi_net_info, _ = self.adb_shell.communicate(b'dumpsys wifi | grep "mNetworkInfo"')

        print(wifi_net_info.decode('utf-8'))

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
        super_user_mode = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                          "root"], capture_output=True)
        super_user_mode.stdout.decode("utf-8")

    def disable_wifi_service(self):
        """Method used to disable WiFi radio"""
        disabled_wifi = subprocess.run(["adb", "shell", "svc wifi disable"], capture_output=True)

        disabled_wifi = disabled_wifi.stdout.decode("utf-8")

        return disabled_wifi

    def enable_wifi_service(self):
        """Method used to enable WiFi radio"""
        enabled_wifi = subprocess.run(["adb", "shell", "svc wifi enable"], capture_output=True)

        enabled_wifi = enabled_wifi.stdout.decode("utf-8")

        return enabled_wifi

    def enable_nfc_service(self):
        """Method used to enable NFC radio"""
        enabled_nfc = subprocess.run(["adb", "shell", "svc nfc enable"])

        enabled_nfc = enabled_nfc.stdout.decode("utf-8")

        return enabled_nfc

    def get_cpu_temperatures(self):
        """Method used to get CPU temperatures"""
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
        cpu_directories = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                          "shell", "find", "/sys/devices/system/cpu",
                                          "-name", "cpu[0-9]*", "-type d", "-maxdepth 1"], capture_output=True)
        cpu_directories = cpu_directories.stdout.decode("utf-8").splitlines()
        cpu_frequencies = list()
        for index, cpu_directory in enumerate(cpu_directories):
            cpu_freq = subprocess.run([f"adb", "-s",  f"{self.serial_number}",
                                       "shell", f"cat {cpu_directory}/cpufreq/cpuinfo_cur_freq"],
                           capture_output=True)
            cpu_freq = cpu_freq.stdout.decode("utf-8")
            cpu_frequencies.append(cpu_freq)

        return cpu_frequencies

    def get_cpu_max_speed(self):
        """Method used to get cpu max speed"""
        cpu_max_speeds = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                        "shell", "cat", "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_max_freq"],
                                       capture_output=True)
        cpu_max_speeds = cpu_max_speeds.stdout.decode("utf-8").splitlines()

        return cpu_max_speeds

    def get_cpu_min_speed(self):
        """Method used to get cpu min speed"""
        cpu_min_speeds = subprocess.run(["adb", "-s", f"{self.serial_number}",
                                         "shell", "cat", "/sys/devices/system/cpu/cpu[0-9]*/cpufreq/cpuinfo_min_freq"],
                                        capture_output=True )
        cpu_min_speeds = cpu_min_speeds.stdout.decode("utf-8").splitlines()

        return cpu_min_speeds
    def get_available_devices(self):
        """Method used to get available devices"""
        adb_devices = subprocess.run(["adb", "devices"], capture_output=True)
        adb_devices = adb_devices.stdout.decode("utf-8").splitlines()
        del adb_devices[0]
        del adb_devices[-1]
        serial_numbers = list()
        regex_to_remove =  r"\t.*"
        for i in range(len(adb_devices)):
            match = re.findall(pattern=regex_to_remove, string=adb_devices[i])
            if match:
                serial_numbers.append(adb_devices[i].strip(match[0]))


        return serial_numbers


if __name__ == "__main__":
    adb = AdbInterface()
    adb.get_cpu_temperatures()