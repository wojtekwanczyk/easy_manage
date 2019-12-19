CHASSIS_MAP = {
    1: 'OTHER'.lower(),
    2: 'UNKNOWN'.lower(),
    3: 'DESKTOP'.lower(),
    4: 'LOW_PROFILE_DESKTOP'.lower(),
    5: 'PIZZA_BOX'.lower(),
    6: 'MINI_TOWER'.lower(),
    7: 'TOWER'.lower(),
    8: 'PORTABLE'.lower(),
    9: 'LAPTOP'.lower(),
    10: 'NOTEBOOK'.lower(),
    11: 'HAND_HELD'.lower(),
    12: 'DOCKING_STATION'.lower(),
    13: 'ALL_IN_ONE'.lower(),
    14: 'SUB_NOTEBOOK'.lower(),
    15: 'SPACE_SAVING'.lower(),
    16: 'LUNCH_BOX'.lower(),
    17: 'MAIN_SERVER_CHASSIS'.lower(),
    18: 'EXPANSION_CHASSIS'.lower(),
    19: 'SUB_CHASSIS'.lower(),
    20: 'BUS_EXPANSION_CHASSIS'.lower(),
    21: 'PERIPHERAL_CHASSIS'.lower(),
    22: 'RAID_CHASSIS'.lower(),
}
CHASSIS_CAPABILITIES_MAP = {
    'intrusion_sensor': 'Physical security sensor',
    'frontpanel_lockout': 'Front panel lockout',
    'diagnostic_interrupt': 'Diagnostic interrupt',
    'power_interlock': 'Power interlock'
}


def map_chassis_capabilities(cap_object):
    "Returns human readable chassis capabilities"
    caps = []
    if cap_object.intrusion_sensor == 1:
        caps.append(CHASSIS_CAPABILITIES_MAP['intrusion_sensor'])
    if cap_object.frontpanel_lockout == 1:
        caps.append(CHASSIS_CAPABILITIES_MAP['frontpanel_lockout'])
    if cap_object.diagnostic_interrupt == 1:
        caps.append(CHASSIS_CAPABILITIES_MAP['diagnostic_interrupt'])
    if cap_object.power_interlock == 1:
        caps.append(CHASSIS_CAPABILITIES_MAP['power_interlock'])
    return caps
