import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi_tools import IpmiTools

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)

class IpmiSystem(AbstractSystem,IpmiTools):

    def __init__(self, name, connector):
        super().__init__(name, connector)

        self.ipmi = connector.ipmi
        self.db_filter = {'_connector': self.connector.name, '_system': self.name}

    def __save_to_db(self):
        self.data['_system'] = self.name
        self.data['_connector'] = self.connector.name
        self.db.systems.update(
            self.db_filter,
            self.data,
            upsert=True)

    def __fetch_from_db(self):
        self.data = self.db.systems.find_one(self.db_filter)

    def get_power_state(self):
        return self.ipmi.get_chassis_status().power_on

