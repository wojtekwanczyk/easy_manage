"Module with class responsible for chassis management through Redfish interface"

import logging
import pprint as pp
from easy_manage.chassis.abstract_chassis import AbstractChassis
from easy_manage.utils.redfish_tools import RedfishTools

LOGGER = logging.getLogger('redfish_chassis')
LOGGER.setLevel(logging.DEBUG)


class RedfishChassis(AbstractChassis, RedfishTools):
    "Class responsible for chassis management through Redfish interface"

    def __init__(self, name, connector, endpoint):
        super().__init__(name, connector)

        self.endpoint = endpoint
        self.thermal = None
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

    def get_thermal_health(self, fetch=True):
        if fetch:
            self.thermal = next(iter(self.fetch('/Thermal').values()))
        return self.find(['Status', 'Health'], data=self.thermal)

    def get_temperature(self, name, fetch=True):
        "In Celsius"
        if fetch:
            self.thermal = next(iter(self.fetch('/Thermal').values()))
        pp.pprint(self.thermal)
        sensor_dict = self.get_dict_containing(name, self.thermal)
        return self.find(['ReadingCelsius'], data=sensor_dict)

    def get_fan_speed(self, name, fetch=True):
        "Percentage speed"
        if fetch:
            self.thermal = next(iter(self.fetch('/Thermal').values()))
        sensor_dict = self.get_dict_containing(name, self.thermal)
        return self.find(['Reading'], data=sensor_dict, strict=True)

    def get_thermal_names(self, thermal_type, fetch=True):
        if fetch:
            self.thermal = next(iter(self.fetch('/Thermal').values()))
        names = []
        for structure in self.thermal[thermal_type]:
            names.append(structure['Name'])
        return names

    def get_temperature_names(self, fetch=True):
        return self.get_thermal_names('Temperatures', fetch)

    def get_fan_names(self, fetch=True):
        return self.get_thermal_names('Fans', fetch)
