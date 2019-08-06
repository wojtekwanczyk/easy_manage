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
        return self.find(['MemorySummary', 'Total'])

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
        return self.find(['Boot', 'AllowableValues'])

    def get_boot_source(self):
        return self.find(['Boot', 'BootSourceOverrideTarget'], True)

    def get_info(self):
        return self.get_main_info()
