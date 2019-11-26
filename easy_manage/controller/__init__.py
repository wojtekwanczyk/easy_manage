from easy_manage.chassis import IpmiChassis, RedfishChassis
from easy_manage.systems import IpmiSystem, RedfishSystem
from easy_manage.shells import BashShell


COMPONENTS = {
    'chassis': {
        'ipmi': IpmiChassis,
        'redfish': RedfishChassis,
    },
    'system': {
        'ipmi': IpmiSystem,
        'redfish': RedfishSystem,
    },
    'shell': {
        'bash': BashShell,
    },
}
