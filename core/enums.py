# Standard Imports

from enum import IntEnum


class BatteryHealth(IntEnum):
    UNKNOWN = 1
    GOOD = 2
    OVERHEAT = 3
    DEAD = 4
    OVERVOLTAGE = 5
    UNSPECIFIED_FAILURE = 6
    COLD = 7

