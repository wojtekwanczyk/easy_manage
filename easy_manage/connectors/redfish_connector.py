"""
RedfishConnector class
"""
import logging

import redfish

from easy_manage.connectors.connector import Connector
from easy_manage.tools.redfish_tools import RedfishTools

LOGGER = logging.getLogger('RedfishConnector')
LOGGER.setLevel(logging.DEBUG)


class RedfishConnector(Connector, RedfishTools):
    " Class for connection through Redfish standard."

    def __init__(self, name, address, db, credentials, port=None):
        super().__init__(name, address, credentials, port)

        self.url = 'https://' + self.address
        self.endpoint = '/redfish/urwav1'
        self.db_filter_name = '_connector'
        self.db_filter = {self.db_filter_name: self.name}
        self.connected = False
        self.client = None
        self.connector = self
        #     for testing
        self.db = db

    def connect(self):
        "Connect to Redfish device(s)"

        try:
            self.client = redfish.redfish_client(
                base_url=self.url,
                username=self.credentials.username,
                password=self.credentials.password)
            self.client.login(auth='session')
            self.connected = True
        except Exception as ex:
            LOGGER.error(f"Error while logging in\n{ex}")
            return False
        return True
