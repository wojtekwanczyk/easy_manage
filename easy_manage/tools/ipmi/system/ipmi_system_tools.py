from .fru import FRU
from .sel import SEL
from .sdr import SDR
from .info import Info



class IpmiSystemTools:
    """
        Class meant for aggregating all of the sub-functionalities listed:
        FRU - Field Replaceable Unit
        SEL - System Event Log
        SDR - Sensor Data Record (Repository)
    """
    def __init__(self, ipmi):
        self.fru = FRU(ipmi)
        self.sel = SEL(ipmi)
        self.sdr = SDR(ipmi)
        self.info = Info(ipmi)