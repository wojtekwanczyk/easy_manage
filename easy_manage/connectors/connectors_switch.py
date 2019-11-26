"It creates connector according to given protocol"

from easy_manage.tools.protocol import Protocol
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.connectors.ssh_connector import SshConnector
from easy_manage.utils.utils import raise_protocol_error


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
