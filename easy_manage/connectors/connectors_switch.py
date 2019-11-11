"It creates connector according to given protocol"

from easy_manage.protocols import Protocols
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.connectors.ssh_connector import SshConnector


def connectors_switch(protocol, address, credentials, port=None):
    "It creates connector according to given protocol and/or port"
    switcher = {
        Protocols.REDFISH: lambda: RedfishConnector(address, credentials),
        Protocols.IPMI: lambda: IpmiConnector(address, credentials),
        Protocols.SSH: lambda: SshConnector(address, credentials)
    }

    switcher_port = {
        Protocols.REDFISH: lambda: RedfishConnector(address, credentials, port),
        Protocols.IPMI: lambda: IpmiConnector(address, credentials, port),
        Protocols.SSH: lambda: SshConnector(address, credentials, port)
    }
    if port:
        return switcher_port.get(protocol, lambda *args, **kwargs: None)()

    return switcher.get(protocol, lambda *args, **kwargs: None)()
