"It creates system according to given protocol"

from easy_manage.protocols import Protocols
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.systems.redfish_system import RedfishSystem


def systems_switch(protocol, connector):
    "It creates system according to given protocol"

    switcher = {
        Protocols.REDFISH: lambda: RedfishSystem(connector, '/redfish/v1/Systems/1'),
        Protocols.IPMI: lambda: IpmiSystem(connector)
    }
    return switcher.get(protocol, lambda *args, **kwargs: None)()
