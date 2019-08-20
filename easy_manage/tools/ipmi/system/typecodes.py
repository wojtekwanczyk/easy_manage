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
