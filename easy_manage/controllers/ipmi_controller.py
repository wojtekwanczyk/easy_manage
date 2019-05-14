import pyipmi
import pyipmi.interfaces

from controller import Controller
from exceptions import NotInitializedError


class IPMIController(Controller):

    def __init__(self, name, address, port):
        super(IPMIController, self).__init__(name, address, port)
        # set initial parameters of object to none
        self.device_id = None
        # set session type to rmcp (ipmitool or other possible), and addresses
        interface = pyipmi.interfaces.create_interface(interface='rmcp')

        # create connection on that interface
        self.ipmi = pyipmi.create_connection(interface)
        self.ipmi.session.set_session_type_rmcp(host=self.address, port=int(self.port))
        # FIXME: username and passowrd prompt to establish session
        self.ipmi.session.set_auth_type_user(username='ipmiusr', password='test')

        # Set target of IPMB to 0x20 MC
        # TODO: Setting the address of the mc to different values
        self.ipmi.target = pyipmi.Target(ipmb_address=0x20)
        self.ipmi.session.establish()

    def show_device_id(self, refresh=True):
        """
        Method for printing device primary options to console

        :param refresh: True <> Get fresh info from server
        :return: None
        """
        # Check whether we want to get from server or want to use retained state
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None and refresh is False:
            raise NotInitializedError('Object has not been initialized with anything, set refresh to true')

        # Below code used only to print out the device ID information
        print('''
        #- ---- BASIC DEVICE INFO ----- #
        Device ID:          %(device_id)s
        Device Revision:    %(revision)s
        Firmware Revision:  %(fw_revision)s
        IPMI Version:       %(ipmi_version)s
        Manufacturer ID:    %(manufacturer_id)d (0x%(manufacturer_id)04x)
        Product ID:         %(product_id)d (0x%(product_id)04x)
        Device Available:   %(available)d
        Provides SDRs:      %(provides_sdrs)d
        Additional Device Support:
        '''[1:-1] % self.device_id.__dict__)

    def show_functions(self, refresh=True):
        """
        Method for showing available features of the device

        :param refresh : True <> Get fresh info from the server
        :return: None
        """
        # Check whether we want to get from server or want to use retained state
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None and refresh is False:
            raise NotInitializedError('Object has not been initialized with anything, set refresh to tru')

        functions = (
            ('SENSOR', 'Sensor Device'),
            ('SDR_REPOSITORY', 'SDR Repository Device'),
            ('SEL', 'SEL Device'),
            ('FRU_INVENTORY', 'FRU Inventory Device'),
            ('IPMB_EVENT_RECEIVER', 'IPMB Event Receiver'),
            ('IPMB_EVENT_GENERATOR', 'IPMB Event Generator'),
            ('BRIDGE', 'Bridge'),
            ('CHASSIS', 'Chassis Device')
        )
        print('# ----- BASIC FUNCTION SUPPORT ----- #')
        for name, desc in functions:
            if self.device_id.supports_function(name):
                print('  %s' % desc)

    def show_firmware_version(self, refresh=True):
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None:
            raise NotInitializedError('Object has not been initialized with anything, set refresh to true')

        if self.device_id.aux is not None:

            print('# -----  FIRMWARE VERSION ----- #\n [%s]' % (
                ' '.join('0x%02x' % d for d in self.device_id.aux)))
        else:
            print('There is no info about this device\'s auxiliary functions')
