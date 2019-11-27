"""
Module with class responsible for management with separate system through Redfish interface
"""

import logging
from easy_manage.tools import RedfishTools
from easy_manage.exceptions import BadHttpResponse
from easy_manage.tools import Protocol, proto_wrap

from .abstract_system import AbstractSystem

LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)


class RedfishSystem(AbstractSystem, RedfishTools):
    "Class responsible for management with separate system through Redfish interface"

    def __init__(self, connector, sys_id=1):
        super().__init__(connector)

        self.endpoint = '/redfish/v1/Systems/' + str(sys_id)
        self.force_fetch = False

    # Basic info

    def get_info(self):
        "Get basic system info"
        return self._get_basic_info()

    def get_oem_info(self):
        "Manufacturer and administrative information"
        return self.find(['Oem'])

    def get_power_state(self):
        return self.find(['PowerState'], force_fetch=True)

    def get_system_health(self):
        return self.find(['Status', 'HealthRollup'], strict=True, force_fetch=True)

    def get_memory_size(self):
        return self.find(['MemorySummary', 'Total'])
        
    def get_power_on_hours(self):
        return self.find(['PowerOnHours'])

    # Power actions

    def reset_action(self, reset_type):
        body = {'ResetType': reset_type}
        res = self.connector.client.post(
            self.endpoint + '/Actions/ComputerSystem.Reset',
            body=body)
        if res.status >= 300:
            raise BadHttpResponse(res.status)

    def restart(self):
        self.reset_action('GracefulRestart')

    def power_off(self):
        self.reset_action('GracefulShutdown')

    def power_on(self):
        self.reset_action('On')

    def force_on(self):
        self.reset_action('ForceOn')

    def force_off(self):
        self.reset_action('ForceOff')

    def force_restart(self):
        self.reset_action('ForceRestart')

    def nmi(self):
        self.reset_action('Nmi')

    # Boot options

    def set_boot_source(self, source, force_fetch=True):
        "We are not allowed to do it from student account :("
        body = {'Boot': {
            'BootSourceOverrideEnabled': 'Once',
            'BootSourceOverrideTarget': source
        }}
        res = self.connector.client.patch(
            self.endpoint,
            body=body)
        if res.status >= 300:
            print(res.status)
            raise BadHttpResponse(res.status)

    def get_allowable_boot_sources(self):
        return self.find(['Boot', 'AllowableValues'])

    def get_boot_source(self):
        return self.find(['Boot', 'BootSourceOverrideTarget'], True)

    # Secure boot keys management

    def _secure_boot_key_reset(self, reset_type):
        ""
        body = {'ResetKeysType': reset_type}
        res = self.connector.client.post(
            self.endpoint + '/SecureBoot/Actions/SecureBoot.ResetKeys',
            body=body)
        if res.status >= 300:
            raise BadHttpResponse(res.status)

    def secure_boot_default_keys(self):
        self._secure_boot_key_reset('ResetAllKeysToDefault')

    def secure_boot_delete_pk(self):
        "Delete Platform Key"
        self._secure_boot_key_reset('DeletePK')

    def secure_boot_delete_keys(self):
        """Delete the content of all UEFI Secure Boot key databases (PK, KEK, DB, DBX).
        This puts the system in Setup Mode"""
        self._secure_boot_key_reset('DeleteAllKeys')

    # Other devices

    def get_coolers(self):
        thermal = self._get_device_info('CooledBy')
        return next(iter(thermal.values()))['Fans']

    def get_chassis(self):
        return self._get_device_info('Chassis')

    def get_power_supplies(self):
        return self._get_device_info('PoweredBy')

    def get_managers(self):
        return self._get_device_info('ManagedBy')

    # Processor management

    def get_processor_count(self):
        return self.find(['ProcessorSummary', 'Count'])

    def get_processor_summary(self):
        "Very short summary for all processors"
        return self.find(['ProcessorSummary'])

    def get_processor_info(self, index):
        "Basic info for specific processor"
        processor_data = self.get_processor_data(index)
        return self._get_basic_info(processor_data)

    def get_processor_data(self, index):
        "Full specific processor data"
        processor_endpoint = self.endpoint + '/Processors/' + str(index)
        return self.get_data(processor_endpoint)

    def _get_cpu_history(self, metric):
        processors_endpoint = self.endpoint + '/Processors'
        processors_data = self.get_data(processors_endpoint)
        history_endpoint = self.find(['History', 'odata'], False, processors_data)
        history_data = self.get_data(history_endpoint)
        final_endpoint = self._get_dict_containing(metric, history_data)
        return self.get_data(final_endpoint['@odata.id'])

    def get_cpu_history_performance(self):
        return self._get_cpu_history('Performance')

    def get_cpu_history_power(self):
        return self._get_cpu_history('Power')
    
    def get_avg_cpu_usage(self):
        return self.get_cpu_history_performance()['Container'][0]['MetricValue']

    def get_min_cpu_power(self):
        return self.get_cpu_history_power()['Container'][0]['MetricValue']

    # Network Interfaces

    def get_network_interface(self, index):
        """Right now it returns structure with links to Chassis'
        Adapters/Ports. We must rethink how do we want to store it."""
        return self.get_data(self.endpoint + '/NetworkInterfaces/' + str(index))

    def get_ethernet_interfaces(self):
        interfaces_data = self.get_data(self.endpoint + '/EthernetInterfaces')
        ethernet_members = self.find(['Members'], True, interfaces_data)
        endpoints = self._endpoint_inception(ethernet_members)
        return self.evaluate_endpoints(endpoints)

    # Other

    def get_storage(self):
        storage = next(iter(self._get_device_info('Storage').values()))
        return storage['Members']

    def get_memory(self):
        return self._get_device_info('Memory')

    def get_pcie_devices(self):
        return self._get_device_info('PCIeDevices')

    def get_pcie_functions(self):
        return self._get_device_info('PCIeFunctions')

    def get_standard_logs(self):
        return self.get_data(self.endpoint + '/LogServices/StandardLog/Entries')

    def get_active_logs(self):
        return self.get_data(self.endpoint + '/LogServices/ActiveLog/Entries')


    # LED manipulation

    def change_led_state(self, state):
        body = {'IndicatorLED': state}
        res = self.connector.client.patch(
            self.endpoint,
            body=body)
        if res.status >= 300:
            raise BadHttpResponse(res.status)

    def led_on(self):
        self.change_led_state('Lit')

    def led_off(self):
        self.change_led_state('Off')

    def led_blinking(self):
        self.change_led_state('Blinking')

    def get_led_state(self):
        return self.find(['IndicatorLED'])

    # Prepared functional chunks of data

    def static_data(self):
        interfaces = self.get_ethernet_interfaces()
        data = {
            'properties': self.get_info(),
            'memory_size_gb': self.get_memory_size(),
            'allowable_boot_sources': self.get_allowable_boot_sources(),
            'fans': self.connector.filter_data(self.get_coolers()),
            'ethernet_interfaces': list(interfaces.values()),
            'storage': self.get_storage(),
            'pci_e': self.connector.filter_data(self.get_pcie_devices()),
        }
        data = self.connector.filter_data(data)
        return proto_wrap(data, Protocol.REDFISH)

    def readings(self):
        data = {
            'power_on_hours': self.get_power_on_hours(),
            'power_state': self.get_power_state(),
            'cpu_usage': self.get_avg_cpu_usage(),
            'cpu_power': self.get_min_cpu_power(),
            'power_health': None,
        }
        return proto_wrap(data, Protocol.REDFISH)
