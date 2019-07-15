"""
Module with class responsible for management with separate system through Redfish interface
"""

import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.redfish_tools import RedfishTools


LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)

class RedfishSystem(AbstractSystem, RedfishTools):
    """
    Class responsible for management with separate system through Redfish interface
    """

    def __init__(self, name, connector, endpoint):
        super().__init__(name, connector)

        self.endpoint = endpoint
        self.db_filter_name = '_system'
        self.db_collection = 'systems'
        self.db_filter = {
            self.connector.db_filter_name: self.connector.name,
            self.db_filter_name: self.name
        }

    def get_power_state(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['PowerState'])

    def get_system_health(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['Status', 'HealthRollup'], strict=True)

    def get_memory_size(self, fetch=False):
        if fetch:
            self.fetch()
        return self.find(['Memory', 'Total'])
