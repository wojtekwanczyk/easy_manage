"Module which aggregates all IPMI system's submodules"
import logging

from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi.ipmi_backend import IpmiBackend
from easy_manage.tools.wrap_with_protocol import proto_wrap
from easy_manage.protocols import Protocols
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
        return proto_wrap(self.backend.system_aggregate(),Protocols.IPMI)

    def static_data(self):
        return proto_wrap(self.backend.system_static_data(),Protocols.IPMI)

    def readings(self):
        return proto_wrap(self.backend.system_readings(),Protocols.IPMI)
