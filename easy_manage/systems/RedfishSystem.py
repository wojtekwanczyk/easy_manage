from easy_manage.systems.AbstractSystem import AbstractSystem
from easy_manage.controllers.RedfishController import RedfishController
import logging
import pprint as pp


LOGGER = logging.getLogger('redfish_system')
LOGGER.setLevel(logging.DEBUG)

class RedfishSystem(AbstractSystem):

    def __init__(self, name, controller, endpoint):
        super().__init__(name, controller)

        self.endpoint = endpoint
        self.db_filter = { '_controller': self.controller.name , '_system': self.name}
    
    def fetch(self, level=1):
        """Fetches data from device through Redfish interface and passes it to database.
        If the session has not been established, then data is fetched from database"""

        if self.controller.connected:
            # fetch through redfish
            self.data = self.controller.update_recurse(self.endpoint, 1)
        elif not self.data:
            self.__fetch_from_db()
        
        # pass data to db
        self.__save_to_db()
        
    
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
        return self.controller.search_recurse('PowerState', self.data)
    
    def get_status(self):
        return self.controller.search_recurse('Status', self.data)

    