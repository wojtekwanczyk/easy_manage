"IPMI chassis module"

from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl
from easy_manage.tools.ipmi.chassis.ipmi_chassis_backend import IpmiChassisBackend


class IpmiChassis():
    "IPMI chassis class, for fetching basic info"

    def __init__(self, ipmi_connector):
        self.backend = IpmiChassisBackend(ipmi_connector)

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
        return self.backend.aggregate()

    def static_data(self):
        return self.backend.static_data()

    def readings(self):
        return self.backend.readings()
