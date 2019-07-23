"Module with class responsible for chassis management through Redfish interface"

import logging
from easy_manage.chassis.abstract_chassis import AbstractChassis
from easy_manage.utils.redfish_tools import RedfishTools
from easy_manage.utils.exceptions import BadHttpResponse

LOGGER = logging.getLogger('redfish_chassis')
LOGGER.setLevel(logging.DEBUG)


class RedfishChassis(AbstractChassis, RedfishTools):
    "Class responsible for chassis management through Redfish interface"

    def __init__(self, name, connector, endpoint):
        super().__init__(name, connector)

        self.endpoint = endpoint
        self.db_filter_name = '_chassis'
        self.db_collection = 'chassis'
        self.db_filter = {
            self.connector.db_filter_name: self.connector.name,
            self.db_filter_name: self.name
        }

    def get_power_state(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['PowerState'])

    def get_health(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['Status', 'Health'], strict=True)
