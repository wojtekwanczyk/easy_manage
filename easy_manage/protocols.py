"Enum for every protocol implemented in app to keep them as constants"

from enum import Enum


class Protocols(Enum):
    REDFISH = 'redfish'
    IPMI = 'ipmi'