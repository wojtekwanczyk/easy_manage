from easy_manage.tools.ipmi.reducers.ipmi_reducer import IpmiReducer
from easy_manage.tools.ipmi.system.SDR.repository import SDRRepository
from easy_manage.tools.ipmi.system.SEL.event_log import SEL
from easy_manage.tools.ipmi.system.bmc_info import BMCInfo
from easy_manage.tools.ipmi.system.fru import FRUChassis, FRU
from easy_manage.tools.ipmi.system.maps.chassis_maps import map_chassis_capabilities
from easy_manage.tools.ipmi.system.sensor import Sensor


class IpmiBackend(FRUChassis):

    def __init__(self, connector):
        ipmi = connector.ipmi
        super().__init__(ipmi)
        self.ipmi = ipmi
        self.FRU = FRU(ipmi, connector.credentials, connector.address)  # This dude is special
        self.SEL = SEL(ipmi)
        self.SDRRepository = SDRRepository(ipmi)
        self.BMCInfo = BMCInfo(ipmi)
        self.Sensor = Sensor(ipmi)

    def chassis_functions(self):
        "Returns chassis capabilities"
        rsp = self.ipmi.send_message_with_name('GetChassisCapabilities')
        caps = map_chassis_capabilities(rsp.capabilities_flags)
        return caps

    def chassis_status(self):
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
        self.ipmi.chassis_control(power_status.value)

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

    def chassis_aggregate(self):
        "Returns aggregate of ipmichassis's info"
        return {
            **self.power_on_hours(),
            **self.chassis_status(),
            'chassis_info': self.chassis_info(),
            'chassis_functions': self.chassis_functions()
        }

    def chassis_static_data(self):
        sys_buf = self.fetch_system_static()
        reducer = IpmiReducer(sys_buf, None)
        return reducer.reduce_chassis_static()

    def chassis_readings(self):
        sys_buf = self.fetch_sensors()
        chass_buf = self.chassis_status()
        reducer = IpmiReducer(sys_buf, chass_buf)
        return reducer.reduce_chassis_reading()

    def system_aggregate(self):
        "Function which aggregates necessary info from IPMI sys, for scraping purposes"
        return {
            'bmc': self.BMCInfo.aggregate(),
            'hardware': self.FRU.aggregate(),
            'events': self.SEL.aggregate(),
            'sensors': self.aggregate_sensor_and_sdrs()  # this also fetches sensor's readings
        }

    def fetch_sensors(self):
        "Function which returns in ipmi-system specific format all of the info only about sensors"
        return {
            'sensors': self.aggregate_sensor_and_sdrs()
        }

    def fetch_system_static(self):
        "Function which returns static system data only"
        return {
            'bmc': self.BMCInfo.aggregate(),
            'hardware': self.FRU.aggregate()
        }

    def aggregate_sensor_and_sdrs(self):
        sdrs = self.SDRRepository.fetch_sdr_object_list()
        aggr = self.Sensor.mass_read_sensor(sdrs)
        for sdr in sdrs:
            aggr[sdr.name]['sensor_info'] = sdr.aggregate()
        return aggr

    def events(self):
        return self.SEL.aggregate()

    def system_static_data(self):
        sys_buf = self.fetch_system_static()
        reducer = IpmiReducer(sys_buf, None)
        return reducer.reduce_system_static()

    def system_readings(self):
        sys_buf = self.fetch_sensors()
        chass_buf = self.power_on_hours()
        reducer = IpmiReducer(sys_buf, chass_buf)
        return reducer.reduce_system_reading()

    def get_power_state(self):
        chass_buf = self.chassis_status()
        reducer = IpmiReducer(None, chass_buf)
        return reducer.get_power_state()
