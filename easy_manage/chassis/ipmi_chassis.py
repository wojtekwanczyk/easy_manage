"IPMI chassis module"
from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl
from easy_manage.tools.ipmi.ipmi_backend import IpmiBackend
from easy_manage.tools import Protocol, proto_wrap

from .abstract_chassis import AbstractChassis


class IpmiChassis(AbstractChassis):
    "IPMI chassis class, for fetching basic info"

    def __init__(self, connector):
        super().__init__(connector)
        self.backend = IpmiBackend(connector)

    def power_up(self):
        "Sets chassis's power up"
        self.backend.set_chassis_power(ChassisControl.POWER_UP)

    def power_cycle(self):
        "Power cycle IPMI function on chassis"
        self.backend.set_chassis_power(ChassisControl.POWER_CYCLE)

    def power_down(self):
        "Powers down the chassis"
        self.backend.set_chassis_power(ChassisControl.POWER_DOWN)

    def hard_reset(self):
        "Performs hard reset on chassis"
        self.backend.set_chassis_power(ChassisControl.HARD_RESET)

    def diagnostic_interrupt(self):
        "Performs diagnostic interrupt on chassis"
        self.backend.set_chassis_power(ChassisControl.DIAGNOSTIC_INTERRUPT)

    def soft_shutdown(self):
        "Performs soft shutdown on chassis"
        self.backend.set_chassis_power(ChassisControl.SOFT_SHUTDOWN)

    def raw_data(self):
        return proto_wrap(self.backend.chassis_aggregate(), Protocol.IPMI)

    def static_data(self):
        return proto_wrap(self.backend.chassis_static_data(), Protocol.IPMI)

    def readings(self):
        return proto_wrap(self.backend.chassis_readings(), Protocol.IPMI)

    def get_power_state(self):
        return self.backend.get_power_state()
