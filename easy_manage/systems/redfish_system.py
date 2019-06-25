from datetime import datetime
import logging
from easy_manage.systems.abstract_system import AbstractSystem


LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)

class RedfishSystem(AbstractSystem):

    def __init__(self, name, controller, endpoint):
        super().__init__(name, controller)

        self.endpoint = endpoint
        self.db_filter = {'_controller': self.controller.name, '_system': self.name}

    def fetch(self, level=1):
        """Fetches data from device through Redfish interface and passes it to database.
        If the session has not been established, then data is fetched from database"""

        if self.controller.connected:
            # fetch through redfish
            self.data = self.controller.update_recurse(self.endpoint, level)
            self.last_update = datetime.now()
            self.__save_to_db()
        elif not self.data:
            self.__fetch_from_db()

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
        state_list = self.controller.search_recurse('PowerState', self.data)
        return True if state_list[0][1] == 'On' else False

    def get_status(self):
        return self.controller.search_recurse('Status', self.data)
