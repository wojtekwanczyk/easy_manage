"Switcher for connector"

from easy_manage.protocols import Protocols
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector


def connectors_switch(protocol, address, credentials, port=None):
    switcher = {
        Protocols.REDFISH: lambda: RedfishConnector(address, credentials),
        Protocols.IPMI: lambda: IpmiConnector(address, credentials)
    }

    switcher_port = {
        Protocols.REDFISH: lambda: RedfishConnector(address, credentials, port),
        Protocols.IPMI: lambda: IpmiConnector(address, credentials, port)
    }
    if port:
        return switcher_port.get(protocol)()

    return switcher.get(protocol)()
