from easy_manage.protocols import Protocols
from easy_manage.chassis.ipmi_chassis import IpmiChassis
from easy_manage.chassis.redfish_chassis import RedfishChassis


def chassis_switch(protocol, connector):
    switcher = {
        Protocols.REDFISH: lambda: RedfishChassis(connector, '/redfish/v1/Chassis/1'),
        Protocols.IPMI: lambda: IpmiChassis(connector)
    }
    return switcher.get(protocol)()
