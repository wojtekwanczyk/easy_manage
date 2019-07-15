import logging
from easy_manage.systems.abstract_system import AbstractSystem
from easy_manage.tools.ipmi.ipmi_system_tools import IpmiSystemTools
from easy_manage.tools.ipmi.ipmi_chassis_tools import IpmiChassisTools

LOGGER = logging.getLogger('ipmi_system')
LOGGER.setLevel(logging.DEBUG)

class IpmiSystem(AbstractSystem):

    def __init__(self, name, connector):
        super().__init__(name, connector)
        self.ipmi = connector.ipmi
        self.db_filter = {'_connector': self.connector.name, '_system': self.name}
        self.system_tools = IpmiSystemTools(connector.ipmi)
        self.chassis_tools = IpmiChassisTools(connector.ipmi)
        
    def __save_to_db(self):
        self.data['_system'] = self.name
        self.data['_connector'] = self.connector.name
        self.db.systems.update(
            self.db_filter,
            self.data,
            upsert=True)

    def __fetch_from_db(self):
        self.data = self.db.systems.find_one(self.db_filter)
