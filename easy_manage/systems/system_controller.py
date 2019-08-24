from easy_manage.protocols import Protocols
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.systems.redfish_system import RedfishSystem


class SystemController:

    def systems_switch(protocol, connector):
        switcher = {
            Protocols.IPMI: RedfishSystem('test_system_redfish', connector,
                                          '/redfish/v1/Systems/1'),
            Protocols.REDFISH: IpmiSystem('test_system_ipmi', connector)
        }

        switcher.get(protocol, "Invalid protocol")
