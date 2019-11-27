"Utility module for connecting to BMC with IPMI"
import logging
import pyipmi
import pyipmi.interfaces
from pyipmi import IpmiTimeoutError

from .connector import Connector

LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)

class IpmiConnector(Connector):

    def __init__(self, address, credentials, port=623):
        super().__init__(address, credentials, port)
        # set initial parameters of object to none
        self.device_id = None
        self.interface = None
        self.ipmi = None
        

    def connect(self, test = False):
        "Function creates connection to given device"
        try:
            interface = pyipmi.interfaces.create_interface(
                interface='ipmitool',
                interface_type='lanplus')
        except Exception as ex:
            LOGGER.error(f"Error while logging in\n{ex}")
            return False

        # create connection on that interface
        ipmi = pyipmi.create_connection(interface)
        ipmi.session.set_session_type_rmcp(
            host=self.address, port=int(self.port))
        ipmi.session.set_auth_type_user(
            username=self.credentials.username,
            password=self.credentials.password)

        ipmi.target = pyipmi.Target(ipmb_address=0x20)
        ipmi.session.establish()
        try:
            ipmi.session.rmcp_ping()    
        except IpmiTimeoutError:
            return False
        if test:
            return True
        self.connected = True
        self.interface = interface
        self.ipmi = ipmi
        return True

        
    def test_connection(self):
        if self.connect(test=True):
            return True
