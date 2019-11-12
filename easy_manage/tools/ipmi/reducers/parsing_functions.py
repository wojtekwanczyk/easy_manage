import re
from logging import getLogger

from easy_manage.tools.ipmi.reducers.utils.path_handlers import extract_by_path

log = getLogger(__name__)


def parse_fan_spd(dictionary):
    return {
        dictionary['sensor_info']['name']: dictionary['reading']['value']
    }


def parse_memsize(dictionary):
    "Gets memory size from an assumed memory component"
    unparsed = extract_by_path(dictionary, ['properties', 'Memory size'])
    number, unit = re.match(r'^(\d+)\s*(\w*)$', unparsed).groups()
    try:
        number = int(number)
        unit = unit.lower()
        if unit != 'mb':
            log.error('Unsupported memory type found, memory will not count in')
        return int(number / 1024)
    except ValueError:
        return 0


def parse_cpu(dictionary):
    "Gets cpu info from an assumed cpu component"
    name = ('_').join(dictionary['Product Asset Tag'].lower().split(' '))
    props = {}
    for k, v in dictionary['properties'].items():
        # new_key = '_'.join(k.split("Product ")[1].lower().split(' '))  # Product Asset tag -> asset_tag
        new_key = k.split("Product ")[1]  # Product Asset tag -> Asset tag
        props[new_key] = v
    return {
        name: props
    }


def parse_memory(dictionary):
    "Gets mem info from an assumed mem component"
    name = dictionary['Part Number'].lower()
    return {
        name: dictionary['properties']
    }


def parse_pci(dictionary):
    name = dictionary['Board Extra']
    name = '_'.join(name.lower().split(' '))
    return {
        name: dictionary['properties']
    }


def parse_pwr(dictionary):
    "Gets power supply info from an assumed pwr_supply component"
    name = ('_').join(dictionary['Board Extra'].lower().split(' '))
    props = {}
    for k, v in dictionary['properties'].items():
        new_key = k.split("Board ")[1]  # Product Asset tag -> Asset tag
        props[new_key] = v
    return {
        name: props
    }


def extract_components(components, validator, parser):
    parsed = list(map(parser, filter(validator, components)))

    ret_dict = {}
    for cmp in parsed:
        ret_dict = {**ret_dict, **cmp}
    return ret_dict
