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