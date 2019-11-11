from easy_manage.tools.ipmi.reducers.ipmi_reducer import IpmiReducer
from easy_manage.tools.ipmi.system.fru import FRU
from easy_manage.tools.ipmi.system.SEL.event_log import SEL
from easy_manage.tools.ipmi.system.SDR.repository import SDRRepository
from easy_manage.tools.ipmi.system.bmc_info import BMCInfo
from easy_manage.tools.ipmi.system.sensor import Sensor


class IpmiSystemBackend:
    def __init__(self, connector):
        from easy_manage.chassis.ipmi_chassis import \
            IpmiChassisBackend  # FIXME: Merge IpmiChassisBackend and IpmiSystemBackend into one class - IPMIBackend
        ipmi = connector.ipmi
        self.FRU = FRU(ipmi, connector.credentials, connector.address)  # This dude is special
        self.SEL = SEL(ipmi)
        self.SDRRepository = SDRRepository(ipmi)
        self.BMCInfo = BMCInfo(ipmi)
        self.Sensor = Sensor(ipmi)
        self.chass_bcknd = IpmiChassisBackend(connector)

    def fetch_all(self):
        "Function which aggregates necessary info from IPMI sys, for scraping purposes"
        return {
            'bmc': self.BMCInfo.aggregate(),
            'hardware': self.FRU.aggregate(),
            # 'events': self.SEL.aggregate(),
            'sensors': self.aggregate_sensor_and_sdrs()  # this also fetches sensor's readings
        }

    def fetch_sensors(self):
        "Function which returns in ipmi-system specific format all of the info only about sensors"
        return {
            'sensors': self.aggregate_sensor_and_sdrs()
        }

    def fetch_static(self):
        "Function which returns static data only"
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

    def static_data(self):
        sys_buf = self.fetch_static()
        reducer = IpmiReducer(sys_buf, None)
        return reducer.reduce_system_static()

    def readings(self):
        sys_buf = self.fetch_sensors()
        chass_buf = self.chass_bcknd.power_on_hours()
        reducer = IpmiReducer(sys_buf, chass_buf)
        return reducer.reduce_system_reading()
