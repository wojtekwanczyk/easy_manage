"Module which exposes certain key-value maps for each of sensor/event reading type code."

THRESHOLD = {
    0x00: 'Lower Non-critical, going low',
    0x01: 'Lower Non-critical, going high',
    0x02: 'Lower Critical, going low',
    0x03: 'Lower Critical, going high',
    0x04: 'Lower Non-recoverable, going low',
    0x05: 'Lower Non-recoverable, going high',
    0x06: 'Upper Non-critical, going low',
    0x07: 'Upper Non-critical, going high',
    0x08: 'Upper Critical, going low',
    0x09: 'Upper Critical, going high',
    0x0A: 'Upper Non-recoverable, going low',
    0x0B: 'Upper Non-recoverable, going high'
}
DISCRETE_02H = {
    0x00: 'Idle',
    0x01: 'Active',
    0x02: 'Busy'
}
DIG_DISCRETE_03H = {
    0x00: 'State Deasserted',
    0x01: 'State Asserted'
}
DIG_DISCRETE_04H = {
    0x00: 'Predictive failure deasserted',
    0x01: 'Predictive failure asserted'
}
DIG_DISCRETE_05H = {
    0x00: 'Limit Not Exceeded',
    0x01: 'Limit Exceeded'
}
DIG_DISCRETE_06H = {
    0x00: 'Performance Met',
    0x01: 'Performance Lags'
}
DISCRETE_07H = {
    0x00: 'Transition to OK',
    0x01: 'Transition to Non-Critical from OK',
    0x02: 'Transition to Critical from less severe',
    0x03: 'Transition to Non-recoverable from less severe',
    0x04: 'Transition to Non-Critical from more severe',
    0x05: 'Transition to Critical from Non-recoverable',
    0x06: 'Transition to Non-recoverable',
    0x07: 'Monitor',
    0x08: 'Informational'
}
DIG_DISCRETE_08H = {
    0x00: 'Device Absent',
    0x01: 'Device Present'
}

DIG_DISCRETE_09H = {
    0x00: 'Device Disabled',
    0x01: 'Device Enabled'
}

DISCRETE_0AH = {
    0x00: 'Running',
    0x01: 'In test',
    0x02: 'Power off',
    0x03: 'On Line',
    0x04: 'Off Line',
    0x05: 'Off Duty',
    0x06: 'Degraded',
    0x07: 'Power Save',
    0x08: 'Install Error'
}

DISCRETE_0BH = {
    0x00: 'Fully Redundant',
    0x01: 'Redundancy Lost',
    0x02: 'Redundancy Degraded',
    0x03: 'Non-Redundant:  Resources Sufficient',
    0x04: 'Non-Redundant - Redundancy Regain: Sufficient Resources Regained',
    0x05: 'Non-Redundant: Resources Insufficient',
    0x06: 'Redundancy Degraded - Redundancy Loss: Not fully Redundant Anymore',
    0x07: 'Redundancy Degraded - Redundancy Regain: Still Not fully Redundant'
}

DISCRETE_0CH = {
    0x00: 'D0 Power State',
    0x01: 'D1 Power State',
    0x02: 'D2 Power State',
    0x03: 'D3 Power State'
}
TYPECODES = {
    0x01: THRESHOLD,
    0x02: DISCRETE_02H,
    0x03: DIG_DISCRETE_03H,
    0x04: DIG_DISCRETE_04H,
    0x05: DIG_DISCRETE_05H,
    0x06: DIG_DISCRETE_06H,
    0x07: DISCRETE_07H,
    0x08: DIG_DISCRETE_08H,
    0x09: DIG_DISCRETE_09H,
    0x0A: DISCRETE_0AH,
    0x0B: DISCRETE_0BH,
    0x0C: DISCRETE_0CH
}
SENSOR_SPECIFIC = {
    0x5: {
        0x00: 'General Chassis Intrusion',
        0x02: 'I/O Card area intrusion',
        0x01: 'Drive Bay intrusion',
        0x03: 'Processor area intrusion',
        0x04: 'LAN Leash Lost (system is unplugged from LAN)',
        0x05: 'Unauthorized dock',
        0x06: 'FAN area intrusion'
    },
    0x6: {
        0x00: 'Secure Mode (Front Panel Lockout) Violation attempt',
        0x01: 'Pre-boot Password Violation - user password',
        0x02: 'Pre-boot Password Violation attempt - setup password',
        0x03: 'Pre-boot Password Violation - network boot password',
        0x04: 'Other pre-boot Password Violation',
        0x05: 'Out-of-band Access Password Violation'
    },
    0x7: {
        0x00: 'IERR',
        0x01: 'Thermal Trip',
        0x02: 'FRB1/BIST failure',
        0x03: 'FRB2/Hang in POST failure (used hang is believed to be due or related to a processor failure. Use System Firmware Progress sensor for other BIOS hangs.)',
        0x04: 'FRB3/Processor Startup/Initialization failure (CPU didn’t start)',
        0x05: 'Configuration Error',
        0x06: 'SM BIOS ‘Uncorrectable CPU-complex Error’',
        0x07: 'Processor Presence detected',
        0x08: 'Processor disabled',
        0x09: 'Terminator Presence Detected',
        0x0A: 'Processor Automatically Throttled (processor throttling triggered by a hardware-based mechanism operating independent from system software, such as automatic thermal throttling or throttling to limit power consumption.)',
        0x0B: 'Machine Check Exception (Uncorrectable)',
        0x0C: 'Correctable Machine Check Error',
    },
    0x8: {
        0x00: 'Presence detected',
        0x01: 'Power Supply Failure detected',
        0x02: 'Predictive Failure',
        0x03: 'Power Supply input lost (AC/DC)',
        0x04: 'Power Supply input lost or out-of-range',
        0x05: 'Power Supply input out-of-range, but present',
        0x06: 'Configuration error',
        0x07: 'Power Supply Inactive (in standby state). Power supply is in a standby state where its main outputs have been automatically deactivated because the load is being supplied by one or more other power supplies.'
    },
    0x9: {
        0x00: 'Power Off / Power Down',
        0x01: 'Power Cycle',
        0x02: '240VA Power Down',
        0x03: 'Interlock Power Down',
        0x04: 'AC lost / Power input lost (The power source for the power unit was lost)',
        0x05: 'Soft Power Control Failure (unit did not respond to request to turn on)',
        0x06: 'Power Unit Failure detected',
        0x07: 'Predictive Failure',
    },
    0xC: {
        0x00: 'Correctable ECC / other correctable memory error',
        0x01: 'Uncorrectable ECC / other uncorrectable memory error',
        0x02: 'Parity',
        0x03: 'Memory Scrub Failed (stuck bit)',
        0x04: 'Memory Device Disabled',
        0x05: 'Correctable ECC / other correctable memory error logging limit reached',
        0x06: 'Presence detected',
        0x07: 'Configuration error',
        0x08: 'Spare',
        0x09: 'Memory Automatically Throttled',
        0x0A: 'Critical Overtemperature',
    },
    0xD: {
        0x00: 'Drive Presence',
        0x01: 'Drive Fault',
        0x02: 'Predictive Failure',
        0x03: 'Hot Spare',
        0x04: 'Consistency Check / Parity Check in progress',
        0x05: 'In Critical Array',
        0x06: 'In Failed Array',
        0x07: 'Rebuild/Remap in progress',
        0x08: 'Rebuild/Remap Aborted (was not completed normally)',
    },
    0xF: {
        0x00: 'System Firmware Error (POST Error)',
        0x01: 'System Firmware Hang',
        0x02: 'System Firmware Progress',
    },
    0x10: {
        0x00: 'Correctable Memory Error Logging Disabled',
        0x01: 'Event ‘Type’ Logging Disabled. Event Logging is disabled for following event/reading type and offset has been disabled.',
        0x02: 'Log Area Reset/Cleared',
        0x03: 'All Event Logging Disabled',
        0x04: 'SEL Full',
        0x05: 'SEL Almost Full',
        0x06: 'Correctable Machine Check Error Logging Disabled',
    },
    0x11: {
        0x00: 'BIOS Watchdog Reset',
        0x01: 'OS Watchdog Reset',
        0x02: 'OS Watchdog Shut Down',
        0x03: 'OS Watchdog Power Down',
        0x04: 'OS Watchdog Power Cycle',
        0x05: 'OS Watchdog NMI / Diagnostic Interrupt',
        0x06: 'OS Watchdog Expired, status only',
        0x07: 'OS Watchdog pre-timeout Interrupt, non-NMI',
    },
    0x12: {
        0x00: 'System Reconfigured',
        0x01: 'OEM System Boot Event',
        0x02: 'Undetermined system hardware failure',
        0x03: 'Entry added to Auxiliary Log',
        0x04: 'PEF Action',
        0x05: 'Timestamp Clock Synch',
    },
    0x13: {
        0x00: 'Front Panel NMI / Diagnostic Interrupt',
        0x01: 'Bus Timeout',
        0x02: 'I/O channel check NMI',
        0x03: 'Software NMI',
        0x04: 'PCI PERR',
        0x05: 'PCI SERR',
        0x06: 'EISA Fail Safe Timeout',
        0x07: 'Bus Correctable Error',
        0x08: 'Bus Uncorrectable Error',
        0x09: 'Fatal NMI (port 61h, bit 7)',
        0x0A: 'Bus Fatal Error',
        0x0B: 'Bus Degraded (bus operating in a degraded performance state)',
    },
    0x14: {
        0x00: 'Power Button pressed',
        0x01: 'Sleep Button pressed',
        0x02: 'Reset Button pressed',
        0x03: 'FRU latch open',
        0x04: 'FRU service request button',
    },
    0x19: {
        0x00: 'Soft Power Control Failure (chip set did not respond to BMC request to change system power state)',
        0x01: 'Thermal trip'
    },
    0x1B: {
        0x00: 'Cable/Interconnect is connected',
        0x01: 'Configuration Error - Incorrect cable connected / Incorrect interconnection'
    },
    0x1D: {
        0x00: 'Initiated by power up',
        0x01: 'Initiated by hard reset',
        0x02: 'Initiated by warm reset',
        0x03: 'User requested PXE boot',
        0x04: 'Automatic boot to diagnostic',
        0x05: 'OS / run-time software initiated hard reset',
        0x06: 'OS / run-time software initiated warm reset',
        0x07: 'System Restart',
    },
    0x1E: {
        0x00: 'No bootable media',
        0x01: 'Non-bootable diskette left in drive',
        0x02: 'PXE Server not found',
        0x03: 'Invalid boot sector',
        0x04: 'Timeout waiting for user selection of boot source',
    },
    0x1F: {
        0x00: 'A: boot completed',
        0x01: 'C: boot completed',
        0x02: 'PXE boot completed',
        0x03: 'Diagnostic boot completed',
        0x04: 'CD-ROM boot completed',
        0x05: 'ROM boot completed',
        0x06: 'Boot completed - boot device not specified',
        0x07: 'Base OS/Hypervisor Installation started',
        0x08: 'Base OS/Hypervisor Installation completed',
        0x09: 'Base OS/Hypervisor Installation aborted',
        0x0A: 'Base OS/Hypervisor Installation failed',
    },
    0x20: {
        0x00: 'Critical stop during OS load/initialization',
        0x01: 'Runtime critical stop (core dump)',
        0x02: 'OS Graceful Stop',
        0x03: 'OS Graceful Shutdown',
        0x04: 'Soft Shutdown initiated by PEF',
        0x05: 'Agent Not Responding. Graceful shutdown request to agent via BMC did not occur due to missing or malfunctioning local agent',
    },
    0x21: {
        0x00: 'Fault Status asserted',
        0x01: 'Identify Status asserted',
        0x02: 'Slot / Connector Device installed/attached',
        0x03: 'Slot / Connector Ready for Device Installation',
        0x04: 'Slot/Connector Ready for Device Removal',
        0x05: 'Slot Power is Off',
        0x06: 'Slot / Connector Device Removal Request',
        0x07: 'Interlock asserted ',
        0x08: 'Slot is Disabled',
        0x09: 'Slot holds spare device',
    },
    0x22: {
        0x00: 'S0 / G0: “working”',
        0x01: 'S1: “sleeping with system h/w & processor context maintained”',
        0x02: 'S2: “sleeping, processor context lost”',
        0x03: 'S3: “sleeping, processor & h/w context lost, memory retained.”',
        0x04: 'S4: “non-volatile sleep / suspend-to disk”',
        0x05: 'S5 / G2: “soft-off”',
        0x06: 'S4 / S5: soft-off, particular S4 / S5 state cannot be determined',
        0x07: 'G3 / Mechanical Off',
        0x08: 'Sleeping in S1, S2, or S3 state',
        0x09: 'G1 sleeping (S1-S4 state cannot be determined)',
        0x0A: 'S5 entered by override',
        0x0B: 'Legacy ON state',
        0x0C: 'Legacy OFF state',
        0x0E: 'Unknown'
    },
    0x23: {
        0x00: 'Timer expired, status only',
        0x01: 'Hard Reset',
        0x02: 'Power Down',
        0x03: 'Power Cycle',
        0x04: 'Reserved',
        0x05: 'Reserved',
        0x06: 'Reserved',
        0x07: 'Reserved',
        0x08: 'Timer interrupt',
    },
    0x24: {
        0x00: 'Platform generated page',
        0x01: 'Platform generated LAN alert',
        0x02: 'Platform Event Trap generated',
        0x03: 'Platform generated SNMP trap',
    },
    0x25: {
        0x00: 'Entity Present',
        0x01: 'Entity Absent',
        0x02: 'Entity Disabled',
    },
    0x27: {
        0x00: 'LAN Heartbeat Lost',
        0x01: 'LAN Heartbeat ',
    },
    0x28: {
        0x00: 'Sensor access degraded or unavailable',
        0x01: 'Controller access degraded or unavailable ',
        0x02: 'Management controller off-line',
        0x03: 'Management controller unavailable',
        0x04: 'Sensor failure',
        0x05: 'FRU failure',
    },
    0x29: {
        0x00: 'battery low (predictive failure)',
        0x01: 'battery failed',
        0x02: 'battery presence detected',
    },
    0x2A: {
        0x00: 'Session Activated',
        0x01: 'Session Deactivated',
        0x02: 'Invalid Username or Password',
        0x03: 'Invalid password disable',
    },
    0x2B: {
        0x00: 'Hardware change detected with associated Entity',
        0x01: 'Firmware or software change detected with associated Entity',
        0x02: '02h Hardware incompatibility detected with associated Entity',
        0x03: '03h Firmware or software incompatibility detected with associated Entity',
        0x04: '04h Entity is of an invalid or unsupported hardware version',
        0x05: 'Entity contains an invalid or unsupported firmware or software version',
        0x06: 'Hardware Change detected with associated Entity was successful',
        0x07: 'Software or F/W Change detected with associated Entity was successful',
    },
    0x2C: {
        0x00: 'FRU Not installed',
        0x01: 'FRU Inactive',
        0x02: 'FRU Activation Requested',
        0x03: 'FRU Activation In Progress',
        0x04: 'FRU Active',
        0x05: 'FRU Deactivation Requested',
        0x06: 'FRU Deactivation In Progress',
        0x07: 'FRU Communication Lost',
    }
}

THRESHOLDS = {
    0: '<= lower non-critical threshold',
    1: '<= lower critical threshold',
    2: '<= lower non-recoverable threshold',
    3: '>= upper non-critical threshold',
    4: '>= upper critical threshold',
    5: '>= upper non-recoverable threshold',
}
