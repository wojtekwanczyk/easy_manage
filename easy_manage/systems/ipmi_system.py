import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi.system.ipmi_system_tools import IpmiSystemTools
from easy_manage.tools.ipmi.chassis.ipmi_chassis_tools import IpmiChassisTools
from easy_manage.tools.ipmi.system.fru import FRU
from easy_manage.tools.ipmi.system.sel import SEL
from easy_manage.tools.ipmi.system.sdr import SDR
from easy_manage.tools.ipmi.system.info import Info
from easy_manage.tools.ipmi.system.sensor import Sensor

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)


class IpmiSystem(AbstractSystem):
    """
        Class meant for aggregating all of the sub-functionalities listed:
        FRU - Field Replaceable Unit
        SEL - System Event Log
        SDR - Sensor Data Record Repository
        Info - basic BMC info
        Sensor - Sensor readings etc.
    """

    def __init__(self, name, connector):
        super().__init__(name, connector)
        self.ipmi = connector.ipmi
        self.db_filter = {
            '_connector': self.connector.name, '_system': self.name}

        self.fru = FRU(self.ipmi)
        self.sel = SEL(self.ipmi)
        self.sdr = SDR(self.ipmi)
        self.info = Info(self.ipmi)
        self.sensor = Sensor(self.ipmi)
