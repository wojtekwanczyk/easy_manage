import logging

from easy_manage.systems.abstract_system import AbstractSystem

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)


class IpmiSystem(AbstractSystem):

    def __init__(self, name, connector):
        super().__init__(name, connector)

        self.ipmi = connector.ipmi
        self.db_filter = {'_connector': self.connector.name, '_system': self.name}

    def __dir__(self):
        return self.methods + ['test']

    def get_power_state(self):
        return self.ipmi.get_chassis_status().power_on

    def get_status(self):
        return self.connector.search_recurse('Status', self.data)

    def test(self):
        print('test')
