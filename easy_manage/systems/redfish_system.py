'''
Module with class responsible for management with separate system through Redfish interface
'''

import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.redfish.redfish_tools import RedfishTools
from easy_manage.utils.exceptions import BadHttpResponse


LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)


class RedfishSystem(AbstractSystem, RedfishTools):
    '''
    Class responsible for management with separate system through Redfish interface
    '''

    def __init__(self, name, connector, endpoint):
        super().__init__(name, connector)

        self.endpoint = endpoint
        self.db_filter_name = '_system'
        self.db_collection = 'systems'
        self.db_filter = {
            self.connector.db_filter_name: self.connector.name,
            self.db_filter_name: self.name
        }

    # Basic info

    def get_info(self):
        return self._get_main_info()

    def get_power_state(self, fetch=True):
        if fetch:
            self._fetch()
        return self._find(['PowerState'])

    def get_system_health(self, fetch=True):
        if fetch:
            self._fetch()
        return self._find(['Status', 'HealthRollup'], strict=True)

    def get_memory_size(self, fetch=False):
        if fetch:
            self._fetch()
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

    def set_boot_source(self, source):
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
        processor_endpoint = self.endpoint + '/Processors/' + str(index)
        processor_data = self.get_data(processor_endpoint)
        return self._get_main_info(processor_data)

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
