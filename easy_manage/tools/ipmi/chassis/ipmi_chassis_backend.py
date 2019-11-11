from easy_manage.tools.ipmi.reducers.ipmi_reducer import IpmiReducer
from easy_manage.tools.ipmi.system.fru import FRUChassis
from easy_manage.tools.ipmi.system.maps.chassis_maps import map_chassis_capabilities


class IpmiChassisBackend(FRUChassis):

    def __init__(self, connector):
        from easy_manage.systems.ipmi_system import \
            IpmiSystemBackend  # FIXME: Merge IpmiChassisBackend and IpmiSystemBackend into one class - IPMIBackend
        ipmi = connector.ipmi
        super().__init__(ipmi)
        self.ipmi = ipmi
        self.system_bcknd = IpmiSystemBackend(connector)

    def functions(self):
        "Returns chassis capabilities"
        rsp = self.ipmi.send_message_with_name('GetChassisCapabilities')
        caps = map_chassis_capabilities(rsp.capabilities_flags)
        return caps

    def status(self):
        "Returns Chasiss status object"
        status = self.ipmi.get_chassis_status()
        return {
            'chassis_status': {
                "power_on": status.power_on,
                "overload": status.overload,
                "interlock": status.interlock,
                "fault": status.fault,
                "control_fault": status.control_fault,
                "restore_policy": status.restore_policy,
                "last_event": status.last_event,
                "chassis_state": status.chassis_state
            }
        }

    def set_chassis_power(self, power_status):
        self.ipmi.chassis_control(power_status)

    def power_on_hours(self):
        "Returns power on hours on chassis"
        poh_rsp = self.ipmi.send_message_with_name('GetPohCounter')
        return {
            'power_on_counter': {
                'minutes_per_count': poh_rsp.minutes_per_count,
                'counter_reading': poh_rsp.counter_reading
            }
        }

    def chassis_info(self):
        "Returns FRU chassis info - "
        return self.fru_chassis_info()

    def aggregate(self):
        "Returns aggregate of ipmichassis's info"
        return {
            **self.power_on_hours(),
            **self.status(),
            'chassis_info': self.chassis_info(),
            'chassis_functions': self.functions()
        }

    def static_data(self):
        sys_buf = self.system_bcknd.fetch_static()
        reducer = IpmiReducer(sys_buf, None)
        return reducer.reduce_chassis_static()

    def readings(self):
        sys_buf = self.system_bcknd.fetch_sensors()
        chass_buf = self.status()
        reducer = IpmiReducer(sys_buf, chass_buf)
        return reducer.reduce_chassis_reading()
