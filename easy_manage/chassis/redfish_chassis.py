"Module with class responsible for chassis management through Redfish interface"

import logging
import pprint as pp
from easy_manage.chassis.abstract_chassis import AbstractChassis
from easy_manage.tools.redfish.redfish_tools import RedfishTools

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

    # Basic info

    def get_oem_info(self):
        "Manufacturer and administrative information"
        self.fetch()
        return self.find(['Oem'])

    def get_info(self):
        return self.get_main_info()

    def get_power_state(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['PowerState'])

    def get_health(self, fetch=True):
        if fetch:
            self.fetch()
        return self.find(['Status', 'Health'], strict=True)

    # Thermal management (fans & temperatures)

    def get_thermal_health(self):
        thermal = self.get_data(self.endpoint + '/Thermal')
        return self.find(['Status', 'Health'], data=thermal)

    def _get_thermal_names(self, thermal_type):
        thermal = self.get_data(self.endpoint + '/Thermal')
        names = []
        for structure in thermal[thermal_type]:
            names.append(structure['Name'])
        return names

    def get_temperature_names(self):
        return self._get_thermal_names('Temperatures')

    def get_fan_names(self):
        return self._get_thermal_names('Fans')

    def get_temperature(self, name):
        "In Celsius"
        thermal = self.get_data(self.endpoint + '/Thermal')
        sensor_dict = self.get_dict_containing(name, thermal)
        return self.find(['ReadingCelsius'], data=sensor_dict)

    def get_fan_speed(self, name):
        "Percentage speed"
        thermal = self.get_data(self.endpoint + '/Thermal')
        sensor_dict = self.get_dict_containing(name, thermal)
        return self.find(['Reading'], data=sensor_dict, strict=True)

    # Power supply management
    def _power_search(self, name):
        power_data = self.get_data(self.endpoint + '/Power')
        return self.find([name], strict=True, data=power_data)

    def get_power_info(self):
        return self._power_search('Oem')

    def get_power_control(self):
        return self._power_search('PowerControl')

    def get_power_supplies(self):
        return self._power_search('PowerSupplies')

    def get_power_supply(self, index):
        odata_id = self.endpoint + '/Power#/PowerSupplies/' + str(index)
        power_data = self.get_data(self.endpoint + '/Power')
        return self.get_dict_containing(odata_id, power_data['PowerSupplies'])

    def get_power_voltages(self):
        return self._power_search('Voltages')

    def get_power_voltage(self, index):
        odata_id = self.endpoint + '/Power#/Voltages/' + str(index)
        power_data = self.get_data(self.endpoint + '/Power')
        return self.get_dict_containing(odata_id, power_data['Voltages'])

    def get_power_redundancy(self):
        return self._power_search('Redundancy')

    # Network Adapters

    def get_network_adapters(self):
        return self.update_recurse(self.endpoint + '/NetworkAdapters')

    # Other devices

    def _get_device_info(self, name):
        "Get device info from Redfish Links"
        endpoints = self.endpoint_inception(self.find([name]))
        data = {}
        for endpoint in endpoints:
            data[endpoint] = self.get_data(endpoint)
        return data

    def get_pcie_devices(self):
        return self._get_device_info('PCIeDevices')

    def get_storage(self):
        return self._get_device_info('Storage')

    def get_drives(self):
        return self._get_device_info('Drives')

    def get_computer_systems(self):
        return self._get_device_info('ComputerSystems')

    def get_managers(self):
        return self._get_device_info('ManagersInChassis')
