"It creates connector according to given protocol"

from easy_manage.tools import Protocol
from easy_manage.connectors import IpmiConnector
from easy_manage.connectors import RedfishConnector
from easy_manage.connectors import SshConnector
from easy_manage.utils import raise_protocol_error


def connectors_switch(protocol, address, credentials, port=None):
    "It creates connector according to given protocol and/or port"
    switcher = {
        Protocol.REDFISH: lambda: RedfishConnector(address, credentials),
        Protocol.IPMI: lambda: IpmiConnector(address, credentials),
        Protocol.BASH: lambda: SshConnector(address, credentials)
    }

    switcher_port = {
        Protocol.REDFISH: lambda: RedfishConnector(address, credentials, port),
        Protocol.IPMI: lambda: IpmiConnector(address, credentials, port),
        Protocol.BASH: lambda: SshConnector(address, credentials, port)
    }
    if port:
        return switcher_port.get(protocol, raise_protocol_error)()

    return switcher.get(protocol, raise_protocol_error)()
