"It creates chassis according to given protocol"
from easy_manage.protocols import Protocols
from easy_manage.chassis.ipmi_chassis import IpmiChassis
from easy_manage.chassis.redfish_chassis import RedfishChassis
from easy_manage.utils.utils import raise_protocol_error


def chassis_switch(protocol, connector):
    "It creates chassis according to given protocol"
    switcher = {
        Protocols.REDFISH: lambda: RedfishChassis(connector, '/redfish/v1/Chassis/1'),
        Protocols.IPMI: lambda: IpmiChassis(connector)
    }
    return switcher.get(protocol, raise_protocol_error)()
