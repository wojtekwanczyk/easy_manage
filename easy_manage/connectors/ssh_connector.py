"""
SshConnector class
"""
import logging
from paramiko import SSHClient, AutoAddPolicy

from .connector import Connector

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class SshConnector(Connector, SSHClient):
    "Class responisbile for connection through ssh protocol"

    def __init__(self, address, credentials, port=None):
        Connector.__init__(self, address, credentials, port)
        SSHClient.__init__(self)

    def connect(self):
        """
        Possible exceptions: BadHostKeyException, AuthenticationException,
        SSHException but it dosn't matter which one it is, just logging it.
        """
        self.set_missing_host_key_policy(AutoAddPolicy())
        try:
            SSHClient.connect(
                self,
                hostname=self.address,
                username=self.credentials.username,
                password=self.credentials.password)
        except Exception as ex:
            LOGGER.critical(ex)
            return False
        self.connected = True
        return True

    def disconnect(self):
        SSHClient.close(self)
        self.connected = False

    def test_connection(self):
        if self.connect():
            self.disconnect()
            return True
        return False
