"Switcher for cpnnector"

from easy_manage.protocols import Protocols
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector


def connectors_switch(protocol, address, credentials):
    switcher = {
        Protocols.REDFISH: lambda: RedfishConnector(
            'test_connector_redfish', address, credentials
        ),
        Protocols.IPMI: lambda: IpmiConnector('test_connector_ipmi', address, credentials)
    }
    return switcher.get(protocol, False)()
