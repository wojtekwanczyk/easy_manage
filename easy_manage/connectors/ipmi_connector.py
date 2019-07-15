import logging
import pyipmi
import pyipmi.interfaces

from .connector import Connector
from .exceptions import NotInitializedError

LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)

class IpmiConnector(Connector):

    def __init__(self, name, address, db, credentials, port=623):
        super().__init__(name, address, db, credentials, port)
        # set initial parameters of object to none
        self.device_id = None
        self.interface = None
        self.ipmi = None
        self.connected = False        

    def connect(self):
        """
            Function creates connection to given device
        """
        
        try:
          self.interface = pyipmi.interfaces.create_interface(
                interface='ipmitool',
                interface_type='lanplus')
        except Exception as ex:
            LOGGER.error(f"Error while logging in\n{ex}")
            return False
        
        # create connection on that interface
        self.ipmi = pyipmi.create_connection(self.interface)
        self.ipmi.session.set_session_type_rmcp(host=self.address, port=int(self.port))
        self.ipmi.session.set_auth_type_user(
            username=self.credentials.username,
            password=self.credentials.password)

        # Set target of IPMB to 0x20 MC
        # TODO: Setting the address of the mc to different values
        self.ipmi.target = pyipmi.Target(ipmb_address=0x20)
        self.ipmi.session.establish()
        self.connected = True
        
        return True

   
