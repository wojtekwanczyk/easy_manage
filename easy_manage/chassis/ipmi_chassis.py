"IPMI chassis module"
from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl
from easy_manage.tools.ipmi.system.fru import FRUChassis
from easy_manage.tools.ipmi.system.maps.chassis_maps import map_chassis_capabilities


class IpmiChassis(FRUChassis):
    "IPMI chassis class, for fetching basic info"

    def __init__(self, ipmi_connector):
        ipmi = ipmi_connector.ipmi
        super().__init__(ipmi)
        self.ipmi = ipmi

    def functions(self):
        "Returns chassis capabilities"
        rsp = self.ipmi.send_message_with_name('GetChassisCapabilities')
        caps = map_chassis_capabilities(rsp.capabilities_flags)
        return caps

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
        poh_rsp = self.ipmi.send_message_with_name('GetPohCounter')
        return {
            'minutes_per_count': poh_rsp.minutes_per_count,
            'counter_reading': poh_rsp.counter_reading
        }

    def chassis_info(self):
        "Returns FRU chassis info - "
        return self.fru_chassis_info()

    def aggregate(self):
        "Returns aggregate of ipmichassis's info"
        return {
            'power_on_counter': self.power_on_hours(),
            'chassis_info': self.chassis_info(),
            'chassis_status': self.status(),
            'chassis_functions': self.functions()
        }

    def ipmi_chassis_data(self):
        if not self.connected:
            raise NotConnectedError("IPMI not connected, data fetch exception")
        return self.ipmi_chass.aggregate()
