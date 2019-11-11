"Module which aggregates all IPMI system's submodules"
import logging

from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi.ipmi_backend import IpmiBackend

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)


class IpmiSystem(AbstractSystem):
    """A simple facade for IPMISystem's backend """

    # pylint: disable=invalid-name

    def __init__(self, connector):
        super().__init__(connector)
        self.backend = IpmiBackend(connector)

    # Defines public API
    def events(self):
        "Fetches and aggregates all events"
        return self.backend.events()

    def raw_data(self):
        return self.backend.system_aggregate()

    def static_data(self):
        return self.backend.system_static_data()

    def readings(self):
        return self.backend.system_readings()
