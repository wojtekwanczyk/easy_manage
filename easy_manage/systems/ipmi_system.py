from datetime import datetime
import logging
from easy_manage.systems.abstract_system import AbstractSystem


LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)

class IpmiSystem(AbstractSystem):

    def __init__(self, name, controller):
        super().__init__(name, controller)

        self.ipmi = controller.ipmi
        self.db_filter = {'_controller': self.controller.name, '_system': self.name}

    def __save_to_db(self):
        self.data['_system'] = self.name
        self.data['_controller'] = self.controller.name
        self.db.systems.update(
            self.db_filter,
            self.data,
            upsert=True)

    def __fetch_from_db(self):
        self.data = self.db.systems.find_one(self.db_filter)

    def get_power_state(self):
        return self.ipmi.get_chassis_status().power_on

    def get_status(self):
        return self.controller.search_recurse('Status', self.data)
