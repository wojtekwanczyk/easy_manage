from easy_manage.connectors.exceptions import NotInitializedError


class Info:
    def __init__(self, ipmi):
        self.ipmi = ipmi
    
    def device_info(self, refresh=True):
        """
        Method for printing device primary options to console

        :param refresh: True <> Get fresh info from server
        :return: None
        """
        # Check whether we want to get from server or want to use retained state
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None and refresh is False:
            raise NotInitializedError(
                'Object has not been initialized with anything, set refresh to true')

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
        # TODO: Parse the data to more human-readable format (it will be used for display)
        return self.device_id.__dict__

    def functions(self, refresh=True):
        """
        Method for fetching available features of the device

        :param refresh : True <> Get fresh info from the server
        :return: None
        """
        # Check whether we want to get from server or want to use retained state
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None and refresh is False:
            raise NotInitializedError(
                'Object has not been initialized with anything, set refresh to tru')

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
        supported_functions = []
        for name, desc in functions:
            if self.device_id.supports_function(name):
                supported_functions.append(name)
        return supported_functions
                

    def firmware_version(self, refresh=False):
        if refresh:
            self.device_id = self.ipmi.get_device_id()
        elif self.device_id is None:
            raise NotInitializedError(
                'Object has not been initialized with anything, set refresh to true')

        if self.device_id.aux is not None:
            print('# -----  FIRMWARE VERSION ----- #\n [%s]' % (
                ' '.join('0x%02x' % d for d in self.device_id.aux)))
        else:
            print('There is no info about this device\'s auxiliary functions')
            