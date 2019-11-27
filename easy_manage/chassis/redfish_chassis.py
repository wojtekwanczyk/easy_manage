"Module with class responsible for chassis management through Redfish interface"

import logging
from easy_manage.tools.redfish.redfish_tools import RedfishTools
from easy_manage.tools.protocol import Protocol, proto_wrap

from .abstract_chassis import AbstractChassis


LOGGER = logging.getLogger('redfish_chassis')
LOGGER.setLevel(logging.DEBUG)

class RedfishChassis(AbstractChassis, RedfishTools):
    "Class responsible for chassis management through Redfish interface"

    def __init__(self, connector, chassis_id=1):
        super().__init__(connector)
        self.endpoint = '/redfish/v1/Chassis/' + str(chassis_id)
        self.thermal = None
        self.force_fetch = False

    # Basic info

    def get_oem_info(self):
        "Manufacturer and administrative information"
        return self.find(['Oem'])

    def get_info(self):
        "Get basic chassis info"
        return self._get_basic_info()

    def get_power_state(self):
        return self.find(['PowerState'], force_fetch=True).upper()

    def get_health(self):
        return self.find(['Status', 'Health'], strict=True, force_fetch=True)

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
        sensor_dict = self._get_dict_containing(name, thermal)
        return self.find(['ReadingCelsius'], data=sensor_dict)

    def get_fan_speed(self, name):
        "Percentage speed"
        thermal = self.get_data(self.endpoint + '/Thermal')
        sensor_dict = self._get_dict_containing(name, thermal)
        return self.find(['Reading'], data=sensor_dict, strict=True)

    def get_temperatures(self):
        temp_dict = {
            name: self.get_temperature(name)
            for name in self.get_temperature_names()}
        return temp_dict

    def get_fans(self):
        fan_dict = {
            name: self.get_fan_speed(name)
            for name in self.get_fan_names()}
        return fan_dict

    # Power supply management
    def _power_search(self, name):
        power_data = self.get_data(self.endpoint + '/Power')
        return self.find([name], strict=True, data=power_data)

    def get_power_info(self):
        return self._power_search('Oem')

    def get_power_control(self):
        data = self._power_search('PowerControl')[0]
        data = self.connector.filter_data(data)
        return data
    
    def get_power_readings(self):
        power_control = self.get_power_control()
        power_utilization = dict(filter(
            lambda elem: "Deprecated" not in elem[0],
            power_control['Oem']['Lenovo']['PowerUtilization'].items()))

        data = {
            'state': self.get_power_state(),
            'allocated_watts': power_control['PowerAllocatedWatts'],
            'metrics': power_control['PowerMetrics'],
            'capacity_watts': power_control['PowerCapacityWatts'],
            'utilization': power_utilization,
            'requested_watts': power_control['PowerRequestedWatts'],
            'consumed_watts': power_control['PowerConsumedWatts'],
        }
        return data

    def get_power_supplies(self):
        return self._power_search('PowerSupplies')

    def get_power_supply(self, index):
        odata_id = self.endpoint + '/Power#/PowerSupplies/' + str(index)
        power_data = self.get_data(self.endpoint + '/Power')
        return self._get_dict_containing(odata_id, power_data['PowerSupplies'])

    def get_power_voltages(self):
        return self._power_search('Voltages')

    def get_power_voltage(self, index):
        odata_id = self.endpoint + '/Power#/Voltages/' + str(index)
        power_data = self.get_data(self.endpoint + '/Power')
        return self._get_dict_containing(odata_id, power_data['Voltages'])

    def get_power_redundancy(self):
        return self._power_search('Redundancy')

    # Network Adapters

    def get_network_adapters(self):
        return self._update_recurse(self.endpoint + '/NetworkAdapters')

    # Other devices

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

    def static_data(self, filter_data=True):
        static_power_supplies = self.get_power_supplies()
        for supply in static_power_supplies:
            del supply['Status']
        data = {
            'power_supplies': static_power_supplies,
            'oem': self.get_oem_info(),
        }
        if filter_data:
            data = self.connector.filter_data(data)
        return proto_wrap(data, Protocol.REDFISH)

    def readings(self):
        power_dict = self.get_power_readings()
        data = {
            'temperatures': self.get_temperatures(),
            'fans': self.get_fans(),
            'power': power_dict,
        }
        return proto_wrap(data, Protocol.REDFISH)
