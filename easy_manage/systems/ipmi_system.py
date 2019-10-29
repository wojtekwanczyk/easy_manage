"Module which aggregates all IPMI system's submodules"
import logging

from easy_manage.systems.abstract_system import AbstractSystem

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
