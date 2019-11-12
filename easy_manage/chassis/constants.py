from enum import Enum


class PowerState(Enum):
    ON = 'ON'
    OFF = 'OFF'

    @classmethod
    def all(cls):
        return [proto.value for proto in cls]
