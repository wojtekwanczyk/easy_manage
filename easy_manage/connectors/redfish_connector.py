"""
RedfishConnector class
"""
import logging
import redfish
from easy_manage.connectors.connector import Connector
from easy_manage.utils.redfish_tools import RedfishTools

LOGGER = logging.getLogger('RedfishConnector')
LOGGER.setLevel(logging.DEBUG)

class RedfishConnector(Connector, RedfishTools):
    """
    Class for data retrieved from connector through
    Redfish standard.
    """

    def __init__(self, name, address, db, credentials, port=None):
        super().__init__(name, address, db, credentials, port)

        self.endpoint = '/redfish/v1'
        self.db_filter_name = '_connector'
        self.db_collection = 'connectors'
        self.db_filter = {self.db_filter_name: self.name}
        self.connected = False
        self.client = None
        self.connector = self
        self.systems = None

    def connect(self):
        "Connect to Redfish device(s)"
        try:
            self.client = redfish.redfish_client(
                base_url=self.url,
                username=self.credentials.username,
                password=self.credentials.password)
            self.client.login(auth='session')
            self.connected = True
        except redfish.rest.v1.RetriesExhaustedError as ex:
            LOGGER.error(f"Error while logging in\n{ex}")
            return False
        return True

    def get_systems(self):
        "Get systems"
        systems = self.find_all('Systems')
        self.systems = self.parse_odata(systems)
        return self.systems
