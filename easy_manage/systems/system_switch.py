"It creates system according to given protocol"

from easy_manage.protocol import Protocol
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.utils.utils import raise_protocol_error


def systems_switch(protocol, connector):
    "It creates system according to given protocol"

    switcher = {
        Protocol.REDFISH: lambda: RedfishSystem(connector, '/redfish/v1/Systems/1'),
        Protocol.IPMI: lambda: IpmiSystem(connector)
    }
    return switcher.get(protocol, raise_protocol_error)()
