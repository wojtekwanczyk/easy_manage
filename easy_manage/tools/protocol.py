from enum import Enum


class ProtocolNotHandled(Exception):
    pass


class Protocol(Enum):
    "Enum for every protocol implemented in app to keep them as constants (More abstract - interface)"
    REDFISH = 'redfish'
    IPMI = 'ipmi'
    BASH = 'bash'

    @classmethod
    def all(cls):
        "Lists all possible protocols"
        return [proto.value for proto in cls]


def proto_wrap(data, proto: Protocol):
    return {
        'payload': data,
        'protocol': proto,
    }
