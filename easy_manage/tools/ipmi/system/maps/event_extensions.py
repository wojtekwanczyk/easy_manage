"Module with functions for parsing event-data"
from collections import defaultdict
from easy_manage.tools.ipmi.system.maps.typecodes import SENSOR_SPECIFIC
SEN_SPEC_EXT_FUNC = {
    0x08: {
        0x06: {
            'parse_ext_3': lambda x: {
                0x0: 'Vendor mismatch',
                0x1: 'Revision mismatch',
                0x2: 'Processor missing',
                0x3: 'Power supply rating mismatch',
                0x4: 'Voltage rating mismatch',
            }.get(x & 0xF, 'reserved')
        }
    },
    0x0C: {
        0x08: {
            'parse_ext_3': lambda x: f'Entity-Relative Module id: {x}'
        }
    },
    0x0F: {
        0x00: {
            'parse_ext_2': lambda x: {
                0x00: 'Unspecified',
                0x01: 'No system memory is physically installed in the system',
                0x02: 'No usable system memory, all installed memory has experienced an unrecoverable failure',
                0x03: 'Unrecoverable hard-disk/ATAPI/IDE device failure',
                0x04: 'Unrecoverable system-board failure.',
                0x05: 'Unrecoverable diskette subsystem failure',
                0x06: 'Unrecoverable hard-disk controller failure',
                0x07: 'Unrecoverable PS/2 or USB keyboard failure',
                0x08: 'Removable boot media not found',
                0x09: 'Unrecoverable video controller failure',
                0x0A: 'No video device detected',
                0x0B: 'Firmware (BIOS) ROM corruption detected',
                0x0C: 'CPU voltage mismatch (processors that share same supply have mismatched voltage requirements)',
                0x0D: 'CPU speed matching failure',
            }.get(x, 'reserved')
        },
        0x02: {
            'parse_ext_2': lambda x: {
                0x00: 'Unspecified',
                0x01: 'Memory initialization',
                0x02: 'Hard-disk initialization',
                0x03: 'Secondary processor(s) initialization',
                0x04: 'User authentication',
                0x05: 'User-initiated system setup',
                0x06: 'USB resource configuration',
                0x07: 'PCI resource configuration',
                0x08: 'Option ROM initialization',
                0x09: 'Video initialization',
                0x0A: 'Cache initialization',
                0x0B: 'SM Bus initialization',
                0x0C: 'Keyboard controller initialization',
                0x0D: 'Embedded controller/management controller initialization',
                0x0E: 'Docking station attachment',
                0x0F: 'Enabling docking station',
                0x10: 'Docking station ejection',
                0x11: 'Disabling docking station',
                0x12: 'Calling operating system wake-up vector',
                0x13: 'Starting operating system boot process',
                0x14: 'Baseboard or motherboard initialization',
                0x16: 'Floppy initialization',
                0x17: 'Keyboard test',
                0x18: 'Pointing device test',
                0x19: 'Primary processor initialization',
            }.get(x, 'reserved')
        }
    },
    0x10: {
        0x00: {
            'parse_ext_2': lambda x: f'Entity-Relative module id: {x}'
        },
        0x01: {
            'parse_ext_2': lambda x: f'Event/Reading Type Code {hex(x)} logging disabled',
            'parse_ext_3': lambda x: f'Disabled event\'s offset: {hex(x & 0x0F)}, {("deassertion ","assertion ")[0x10 & x]} events, for {("not "," ")[0x20 & x]} all events of this type'
        },
        0x05: {
            'parse_ext_3': lambda x: f'SEL is {(x / 100)* 100}% full'
        },
        0x06: {
            'parse_ext_2': lambda x: f'Processor\'s associated instance/entity id: {hex(x)}',
            'parse_ext_3': lambda x: f'Given id is: {("ipmi entity instance number","vendor-specific instance number")[0x80 & x]}',
        }

    },
    0x12: {
        0x03: {
            'parse_ext_2': lambda x: f'Log entry action: {LOG_ENTRY_ACTIONS.get(0xF0 & x ,"reserved")}, log type: {LOG_TYPES.get(0x0F & x, "reserved")}'
        },
        0x04: {
            'parse_ext_2': lambda x: f'PEF actions on-event-match will be taken: {", ".join(map_pef_actions(x))}'
        },
        0x05: {
            'parse_ext_2': lambda x: f'Event is {("first","second")[0x80 & x ]} of pair. {TIMESTAMP_CLOCK_TYPES[0x0F & x ]} updated'
        }
    },
    0x19: {
        0x00: {
            'parse_ext_2': lambda x: 'Requested power state: ' + PWR_STATES[x],
            'parse_ext_3': lambda x: 'Power state at time of request: ' + PWR_STATES[x],
        }
    },
    0x1D: {
        0x7: {
            'parse_ext_2': lambda x: 'Restart cause: ' + {
                0x00: 'unknown',
                0x01: 'Chassis Control command',
                0x02: 'reset via pushbutton',
                0x03: 'power-up via power pushbutton',
                0x04: 'Watchdog expiration',
                0x05: 'OEM',
                0x06: 'automatic power-up on AC being applied due to ‘always restore’ power restore policy',
                0x07: 'automatic power-up on AC being applied due to ‘restore previous power state’ power restore policy',
                0x08: 'reset via PEF',
                0x09: 'power-cycle via PEF',
                0x0A: 'soft reset',
                0x0B: 'power-up via RTC',
            }.get(x & 0x0F, 'reserved'),
            'parse_ext_3': lambda x: f'Channel number used to deliver command that generated restart: {hex(x)}'
        }
    },
    0x21: {
        0x09: {
            'parse_ext_2': lambda x: 'Slot/Connector type: ' + {
                0: 'PCI',
                1: 'Drive Array',
                2: 'External Peripheral Connector',
                3: 'Docking',
                4: 'other standard internal expansion slot',
                5: 'slot associated with entity specified by Entity ID for sensor',
                6: 'AdvancedTCA',
                7: 'DIMM/memory device',
                8: 'FAN',
                9: 'PCI ExpressTM',
                10: 'SCSI (parallel) 11 SATA / SAS',
            }.get(0x7F & x, 'reserved'),
            'parse_ext_3': lambda x: f'Slot/Connector number: hex:"{hex(x)}", integer: "{x}"'
        }
    },
    0x23: {
        0x08: {
            'parse_ext_2': lambda x: f'Interrupt type: {INTERRUPT_TYPES.get(0xF0 & x,"reserved")}, Timer use at expiration: {TIMER_USE_AT_EXP.get(0x0F & x,"reserved")}'
        }
    },
    0x28: {
        0x04: {
            'parse_ext_2': lambda x: f'Sensor number: hex: {hex(x)}, int: {x}'
        },
        0x05: {
            'parse_ext_2': lambda x: f'Device is {("not","")[0x80 & x]} a logical FRU device, LUN for Master Write-Read command or FRU Command: {hex(0x18 & x)}, private bus ID: {hex(0x07 & x)} (last two are zeros, if device not intelligent/directly on IPMB)',
            'parse_ext_3': lambda x: f'FRU device ID within the controller that generated the event: {hex(x)} (Or i2c slave address (bus-relative), or IPMB slave address (also bus-relative): { 0xFE & x }) '
        }
    },
    0x2A: {
        0x03: {
            'parse_ext_2': lambda x: f'ID for user that activated session: {0x1F & x}',
            'parse_ext_3': lambda x: f'Deactivation cause: {DEACTIVATION_CAUSES[0x30 & x]}, channel number session was activated/deactivated over: {0xF & x}'
        }
    },
    0x2B: defaultdict(lambda: VERSION_CHANGE_LAMBDA),
    0x2C: defaultdict(lambda: FRU_STATE_CAUSE_LAMBDA)
}

LOG_ENTRY_ACTIONS = {
    0x00: 'entry added',
    0x01: 'entry added because event did not be map to standard IPMI event',
    0x02: 'entry added along with one or more corresponding SEL entries',
    0x03: 'log cleared',
    0x04: 'log disabled',
    0x05: 'log enabled',
}
LOG_TYPES = {
    0x0: 'MCA Log',
    0x1: 'OEM1',
    0x2: 'OEM2',
}
TIMESTAMP_CLOCK_TYPES = {
    0x00: 'SEL Timestamp Clock',
    0x01: 'SDR Timestamp Clock',
}
PWR_STATES = {
    0x00: 'S0 / G0 “working”',
    0x01: 'S1 “sleeping with system h/w & processor context maintained”',
    0x02: 'S2 “sleeping, processor context lost”',
    0x03: 'S3 “sleeping, processor & h/w context lost, memory retained.”',
    0x04: 'S4 “non-volatile sleep / suspend-to disk”',
    0x05: 'S5 / G2 “soft-off”',
    0x06: 'S4 / S5 soft-off, particular S4 / S5 state cannot be determined',
    0x07: 'G3 / Mechanical Off',
    0x08: 'Sleeping in an S1, S2, or S3 states (particular S1, S2, S3 state cannot be determined)',
    0x09: 'G1 sleeping (S1-S4 state cannot be determined)',
    0x0A: 'S5 entered by override',
    0x0B: 'Legacy ON state',
    0x0C: 'Legacy OFF state',
    0x0D: 'reserved',
}
INTERRUPT_TYPES = {
    0x00: 'none',
    0x01: 'SMI',
    0x02: 'NMI',
    0x03: 'Messaging Interrupt',
    0x0F: 'unspecified',
}
TIMER_USE_AT_EXP = {
    0x00: 'reserved',
    0x01: 'BIOS FRB2',
    0x02: 'BIOS/POST',
    0x03: 'OS Load',
    0x04: 'SMS/OS',
    0x05: 'OEM',
    0x0F: 'unspecified',
}
DEACTIVATION_CAUSES = {
    0b00: 'Session deactivatation cause unspecified. This value is also used for Session Activated events.',
    0b01: 'Session deactivated by Close Session command',
    0b10: 'Session deactivated by timeout',
    0b11: 'Session deactivated by configuration change',
}
VERSION_CHANGE_LAMBDA = {
    'parse_ext_2': lambda x: 'Version change type: ' + {
        0x00: 'unspecified',
        0x01: 'management controller device ID (change in one or more fields from ‘Get Device ID’)',
        0x02: 'management controller firmware revision',
        0x03: 'management controller device revision',
        0x04: 'management controller manufacturer ID',
        0x05: 'management controller IPMI version',
        0x06: 'management controller auxiliary firmware ID',
        0x07: 'management controller firmware boot block',
        0x08: 'other management controller firmware',
        0x09: 'system firmware (EFI / BIOS) change',
        0x0A: 'SMBIOS change',
        0x0B: 'operating system change',
        0x0C: 'operating system loader change',
        0x0D: 'service or diagnostic partition change',
        0x0E: 'management software agent change',
        0x0F: 'management software application change',
        0x10: 'management software middleware change',
        0x11: 'programmable hardware change (e.g. FPGA)',
        0x12: 'board/FRU module change (change of a module plugged into associated entity)',
        0x13: 'board/FRU component change (addition or removal of a replaceable component on the board/FRU that is not tracked as a FRU)',
        0x14: 'board/FRU replaced with equivalent version',
        0x15: 'board/FRU replaced with newer version',
        0x16: 'board/FRU replaced with older version',
        0x17: 'board/FRU hardware configuration change (e.g. strap, jumper, cable change, etc.)',
    }[x]
}
FRU_STATE_CAUSE_LAMBDA = {
    'parse_ext_2': lambda x: f'FRU state change cause: { FRU_STATE_CAUSES.get(0xF0 & x,"reserved")}, previous state: { SENSOR_SPECIFIC[0x2C][0x0F & x]}'
}
FRU_STATE_CAUSES = {
    0x00: 'Normal State Change',
    0x01: 'Change Commanded by software external to FRU. 2h = State Change due to operator changing a Handle latch',
    0x03: 'State Change due to operator pressing the hot swap push button',
    0x04: 'State Change due to FRU programmatic action. 5h = Communication Lost',
    0x06: 'Communication Lost due to local failure',
    0x07: 'State Change due to unexpected extraction',
    0x08: 'State Change due to operator intervention/update. 9h = Unable to compute IPMB address',
    0x0A: 'Unexpected Deactivation',
    0x0F: 'State Change, Cause Unknown',
}


def map_pef_actions(x):
    pef_actions_binstr = bin(x)[4:][::-1]  # 2 first are reserved
    actions = [
        'Diagnostic Interrupt (NMI)',
        'OEM action',
        'Power cycle',
        'Reset',
        'Power off',
        'Alert',
    ]
    actions.reverse()
    return [actions[ind] for ind, val in enumerate(pef_actions_binstr) if val == '1']
