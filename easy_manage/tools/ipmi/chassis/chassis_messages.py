from enum import Enum


class ChassisControl(Enum):
    "Chassis control values, correspond to codes in control method"
    POWER_DOWN = 0
    POWER_UP = 1
    POWER_CYCLE = 2
    HARD_RESET = 3
    DIAGNOSTIC_INTERRUPT = 4
    SOFT_SHUTDOWN = 5
