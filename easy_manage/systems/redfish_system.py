"""
Module with class responsible for management with separate system through Redfish interface
"""

from datetime import datetime
import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.redfish.redfish_tools import RedfishTools


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
        self.db_filter = {
            self.connector.db_filter_name: self.connector.name,
            self.db_filter_name: self.name
        }

    def get_power_state(self):
        self.fetch(self.db_filter_name)
        state_list = self.connector.search_recurse('PowerState', self.data)
        print(f"STATES: {state_list}")
        return state_list[0][1] == 'On'

    def get_status(self):
        return self.connector.search_recurse('Status', self.data)
