"""
SshConnector class
"""
import logging
from paramiko import SSHClient, AutoAddPolicy
from easy_manage.connectors.connector import Connector

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class SshConnector(Connector, SSHClient):
    "Class responisbile for connection through ssh protocol"

    def __init__(self, name, address, credentials, port=None):
        Connector.__init__(self, name, address, credentials, port)
        SSHClient.__init__(self)

    def connect(self):
        self.set_missing_host_key_policy(AutoAddPolicy())
        SSHClient.connect(
            self,
            hostname=self.address,
            username=self.credentials.username,
            password=self.credentials.password)
        self.connected = True

    def disconnect(self):
        SSHClient.close(self)

    def test_connection(self):
        """
        Possible exceptions: BadHostKeyException, AuthenticationException,
        SSHException but it dosn't matter which one it is, just logging it.
        """
        try:
            self.connect()
        except Exception as ex:
            LOGGER.critical(ex)
            return False
        self.disconnect()
        return True
