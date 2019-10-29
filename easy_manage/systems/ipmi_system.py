"Module which aggregates all IPMI system's submodules"
import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi.system.fru import FRU
from easy_manage.tools.ipmi.system.SEL.event_log import SEL
from easy_manage.tools.ipmi.system.SDR.repository import SDRRepository
from easy_manage.tools.ipmi.system.bmc_info import BMCInfo
from easy_manage.tools.ipmi.system.sensor import Sensor

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)


class IpmiSystem(AbstractSystem):
    """
        Class meant for aggregating all of the sub-functionalities listed:

        FRU - Field Replaceable Unit
        SEL - System Event Log
        SDR - Sensor Data Record Repository
        BMCInfo - basic BMC info
        Sensor - Sensor readings retrieval
    """
    # pylint: disable=invalid-name

    def __init__(self, name, connector):
        super().__init__(name, connector)
        ipmi = connector.ipmi
        self.FRU = FRU(ipmi, connector.credentials, connector.address)  # This dude is special
        self.SEL = SEL(ipmi)
        self.SDRRepository = SDRRepository(ipmi)
        self.BMCInfo = BMCInfo(ipmi)
        self.Sensor = Sensor(ipmi)

    def aggregate(self):
        "Function which aggregates necessary info from IPMI sys, for scraping purposes"
        return {
            'bmc': self.BMCInfo.aggregate(),
            'hardware': self.FRU.aggregate(),
            'events': self.SEL.aggregate(),
            'sensors': self._aggregate_sensor_and_sdrs()  # this also fetches sensor's readings
        }

    def _aggregate_sensor_and_sdrs(self):
        sdrs = self.SDRRepository.fetch_sdr_object_list()
        aggr = self.Sensor.mass_read_sensor(sdrs)
        for sdr in sdrs:
            aggr[sdr.name]['sensor_info'] = sdr.aggregate()
        return aggr

    def fetch_sensors(self):
        "Fetches and aggregates all of sensor's data"
        return self._aggregate_sensor_and_sdrs()

    def fetch_events(self):
        "Fetches and aggregates all events"
        return self.SEL.aggregate()
