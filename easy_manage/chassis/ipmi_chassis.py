"IPMI chassis module"
from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl


class IpmiChassisTools:
    "IPMI chassis class, for fetching basic info"

    def __init__(self, ipmi):
        self.ipmi = ipmi

    def functions(self):
        "Returns chassis capabilities"
        # TODO: Test this
        return self.ipmi.send_message_with_name('GetChassisCapabilities')

    def status(self):
        "Returns Chasiss status object"
        # TODO: Check return object
        return self.ipmi.get_chassis_status()

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
        return self.ipmi.send_message_with_name('GetPohCounter')

    # GetPowerLevel
        # GetFanSpeedProperties
        # SetFanLevel
        # GetFanLevel
