"""
Module with class responsible for management with separate system through Redfish interface
"""

import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.redfish.redfish_tools import RedfishTools
from easy_manage.utils.exceptions import BadHttpResponse

LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)


class RedfishSystem(AbstractSystem, RedfishTools):
    "Class responsible for management with separate system through Redfish interface"

    def __init__(self, name, connector, endpoint):
        super().__init__(name, connector)

        self.endpoint = endpoint
        self.db_filter_name = '_system'
        self.db_collection = 'systems'
        self.force_fetch = False
        self.db_filter = {
            self.connector.db_filter_name: self.connector.name,
            self.db_filter_name: self.name
        }

    # Basic info

    def get_info(self):
        "Get basic system info"
        return self._get_basic_info()

    def get_oem_info(self):
        "Manufacturer and administrative information"
        return self._find(['Oem'])

    def get_power_state(self):
        return self._find(['PowerState'], force_fetch=True)

    def get_system_health(self):
        return self._find(['Status', 'HealthRollup'], strict=True, force_fetch=True)

    def get_memory_size(self):
        return self._find(['MemorySummary', 'Total'])

    # Power actions

    def reset_action(self, reset_type):
        body = {'ResetType': reset_type}
        res = self.connector.client.post(
            self.endpoint + '/Actions/ComputerSystem.Reset',
            body=body)
        if res.status >= 300:
            raise BadHttpResponse(res.request)

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
            raise BadHttpResponse(str(res.status) + '\n' + str(res.request))

    def get_allowable_boot_sources(self):
        return self._find(['Boot', 'AllowableValues'])

    def get_boot_source(self):
        return self._find(['Boot', 'BootSourceOverrideTarget'], True)

    # Secure boot keys management

    def _secure_boot_key_reset(self, reset_type):
        ""
        body = {'ResetKeysType': reset_type}
        res = self.connector.client.post(
            self.endpoint + '/SecureBoot/Actions/SecureBoot.ResetKeys',
            body=body)
        if res.status >= 300:
            raise BadHttpResponse(res.request)

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
        return self._get_device_info('CooledBy')

    def get_chassis(self):
        return self._get_device_info('Chassis')

    def get_power_supplies(self):
        return self._get_device_info('PoweredBy')

    def get_managers(self):
        return self._get_device_info('ManagedBy')

    # Processor management

    def get_processor_summary(self):
        "Very short summary for all processors"
        return self._find(['ProcessorSummary'])

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
        history_endpoint = self._find(['History', 'odata'], False, processors_data)
        history_data = self.get_data(history_endpoint)
        final_endpoint = self._get_dict_containing(metric, history_data)
        return self.get_data(final_endpoint['@odata.id'])

    def get_cpu_history_performance(self):
        return self._get_cpu_history('Performance')

    def get_cpu_history_power(self):
        return self._get_cpu_history('Power')

    # Network Interfaces

    def get_network_interface(self, index):
        """Right now it returns structure with links to Chassis' 
        Adapters/Ports. We must rethink how do we want to store it."""
        return self.get_data(self.endpoint + '/NetworkInterfaces/' + str(index))

    def get_ethernet_interfaces(self):
        interfaces = self.get_data(self.endpoint + '/EthernetInterfaces')
        endpoints = self._endpoint_inception(self._find(['Members'], False, interfaces))
        data = {}
        for endpoint in endpoints:
            data[endpoint] = self.get_data(endpoint)
        return data

    # Other

    def get_storage(self):
        return self._get_device_info('Storage')

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
