"Module for fetching basic system info"
from easy_manage.exceptions import NotInitializedError


class BMCInfo:
    "Class for fetching basic system info"
    BMC_FUNCTIONS = (
        ('SENSOR', 'Sensor Device'),
        ('SDR_REPOSITORY', 'SDR Repository Device'),
        ('SEL', 'SEL Device'),
        ('FRU_INVENTORY', 'FRU Inventory Device'),
        ('IPMB_EVENT_RECEIVER', 'IPMB Event Receiver'),
        ('IPMB_EVENT_GENERATOR', 'IPMB Event Generator'),
        ('BRIDGE', 'Bridge'),
        ('CHASSIS', 'Chassis Device')
    )

    def __init__(self, ipmi):
        self._ipmi = ipmi
        self.device_id = None

    @property
    def device_info(self):
        "Method which returns bmc options"
        self.device_id = self._ipmi.get_device_id()
        bmc_info = self.device_id.__dict__
        bmc_info['fw_revision'] = bmc_info['fw_revision'].version_to_string()
        bmc_info['ipmi_version'] = bmc_info['ipmi_version'].version_to_string()
        return bmc_info

    @property
    def functions(self):
        "Method for fetching available features of the bmc device"
        self.device_id = self._ipmi.get_device_id()
        supported_functions = []
        for name, _ in BMCInfo.BMC_FUNCTIONS:
            if self.device_id.supports_function(name):
                supported_functions.append(name)
        return supported_functions

    @property
    def firmware_version(self):
        """
        Method for fetching firmware version of the device
        :return: String
        """

        self.device_id = self._ipmi.get_device_id()

        if self.device_id.aux is not None:
            return ' '.join('0x%02x' % d for d in self.device_id.aux)
        return 'undefined'

    def aggregate(self):
        "Function which aggregates bmc's info, for scraping purposes"

        return {
            'bmc_firmware_version': self.firmware_version,
            'bmc_functions': self.functions,
            'bmc_info': self.device_info
        }
