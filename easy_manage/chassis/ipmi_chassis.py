"IPMI chassis module"
from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl
from easy_manage.tools.ipmi.system.fru import FRUChassis


class IpmiChassis(FRUChassis):
    "IPMI chassis class, for fetching basic info"
    # TODO: Determine whether to merge chassis info and chassis status into one - or leave it till we have interface definition

    def __init__(self, ipmi):
        super().__init__(ipmi)
        self.ipmi = ipmi

    def functions(self):
        "Returns chassis capabilities"
        # TODO: Test this
        return self.ipmi.send_message_with_name('GetChassisCapabilities')

    def status(self):
        "Returns Chasiss status object"
        status = self.ipmi.get_chassis_status()
        return {
            "power_on": status.power_on,
            "overload": status.overload,
            "interlock": status.interlock,
            "fault": status.fault,
            "control_fault": status.control_fault,
            "restore_policy": status.restore_policy,
            "last_event": status.last_event,
            "chassis_state": status.chassis_state
        }

    def __set_chassis_power(self, power_status):
        self.ipmi.chassis_control(power_status)

    def power_up(self):
        "Sets chassis's power up"
        self.__set_chassis_power(ChassisControl.POWER_UP)

    def power_cycle(self):
        "Power cycle IPMI function on chassis"
        # TODO Check this out
        self.__set_chassis_power(ChassisControl.POWER_CYCLE)

    def power_down(self):
        "Powers down the chassis"
        self.__set_chassis_power(ChassisControl.POWER_DOWN)

    def hard_reset(self):
        "Performs hard reset on chassis"
        self.__set_chassis_power(ChassisControl.HARD_RESET)

    def diagnostic_interrupt(self):
        "Performs diagnostic interrupt on chassis"
        self.__set_chassis_power(ChassisControl.DIAGNOSTIC_INTERRUPT)

    def soft_shutdown(self):
        "Performs soft shutdown on chassis"
        self.__set_chassis_power(ChassisControl.SOFT_SHUTDOWN)

    def power_on_hours(self):
        "Returns power on hours on chassis"
        # TODO: Test this
        return self.ipmi.send_message_with_name('GetPohCounter')

    def chassis_info(self):
        "Returns FRU chassis info - "
        return self.fru_chassis_info()
