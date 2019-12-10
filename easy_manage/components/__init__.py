from easy_manage.chassis import IpmiChassis, RedfishChassis
from easy_manage.systems import IpmiSystem, RedfishSystem
from easy_manage.shells import BashShell


COMPONENTS = {
    'chassis': {
        'redfish': RedfishChassis,
        'ipmi': IpmiChassis,
    },
    'system': {
        'redfish': RedfishSystem,
        'ipmi': IpmiSystem,
    },
    'shell': {
        'bash': BashShell,
    },
}
