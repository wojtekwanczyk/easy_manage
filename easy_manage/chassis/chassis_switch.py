"It creates chassis according to given protocol"
from easy_manage.protocol import Protocol
from easy_manage.chassis.ipmi_chassis import IpmiChassis
from easy_manage.chassis.redfish_chassis import RedfishChassis
from easy_manage.utils.utils import raise_protocol_error


def chassis_switch(protocol, connector):
    "It creates chassis according to given protocol"
    switcher = {
        Protocol.REDFISH: lambda: RedfishChassis(connector, '/redfish/v1/Chassis/1'),
        Protocol.IPMI: lambda: IpmiChassis(connector)
    }
    return switcher.get(protocol, raise_protocol_error)()
