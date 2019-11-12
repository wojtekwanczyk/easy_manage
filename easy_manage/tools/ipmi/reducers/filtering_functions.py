import re

from easy_manage.tools.ipmi.reducers.constants.exceptions import InvalidPathError
from easy_manage.tools.ipmi.reducers.utils.path_handlers import bare_validate_paths


def is_memory(dictionary):
    "Checks if given dictionary looks like memory component"
    try:
        bare_validate_paths(dictionary, ['properties', 'Memory size'])
    except InvalidPathError:
        return False
    return True


def is_cpu(dictionary):
    "Checks if given dictionary looks like cpu component"
    try:
        bare_validate_paths(dictionary, ['Product Asset Tag'])
    except InvalidPathError:
        return False
    return True


def is_pci(dictionary):
    "Checks if given dictionary looks like a pci-related component"
    try:
        bare_validate_paths(dictionary, ['Board Extra'])
    except InvalidPathError:
        return False
    desc = dictionary['Board Extra'].lower()
    if re.match(r'.*?pci.*?', desc):
        return True
    return False


def is_pwr(dictionary):
    "Checks if given dictionary looks like a power-supply component"
    try:
        bare_validate_paths(dictionary, ['Board Extra'])
    except InvalidPathError:
        return False
    desc = dictionary['Board Extra'].lower()
    if re.match(r'.*?psu.*?', desc):
        return True
    return False


def is_fan(dictionary):
    "Checks whether given sensor is a fan"
    try:
        bare_validate_paths(dictionary, ['sensor_info', 'sensor_type'])
        bare_validate_paths(dictionary, ['sensor_info', 'name'])
        bare_validate_paths(dictionary, ['reading', 'value'])  # just to be sure
    except InvalidPathError:
        return False
    return dictionary['sensor_info']['sensor_type'] == 'fan'
