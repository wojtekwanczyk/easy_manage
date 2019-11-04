"Class for fetching data from FRU (BMC/motherboard in this case)"
import subprocess
from subprocess import CalledProcessError
import logging
import re

from easy_manage.tools.ipmi.system.maps.chassis_maps import CHASSIS_MAP
log = logging.getLogger(__name__)


class FRUInventoryOwner:
    "Base class for FRU inventory utilization"

    def __init__(self, ipmi):
        self._ipmi = ipmi
        self.fru_inventory = None

    def _fetch_inventory(self):
        "Method which fetches data from the fru inventory"
        self.fru_inventory = self._ipmi.get_fru_inventory()


class FRU(FRUInventoryOwner):
    "Class for easier access to FRU data"
    BOARD_EXTRA = 'Board Extra'
    COMPONENT_HEADER_REGEXP = re.compile(r"^(.*) \(ID (\d+)\)$")
    PROPERTY_LINE_REGEXP = re.compile(r"^(.*?)\s*:\s*(.*)$")

    def __init__(self, ipmi, credentials, address):
        super().__init__(ipmi)
        self._ipmitool_baseargs = ['-H', address, '-U', credentials.username, '-P', credentials.password, '-I', 'lanplus']

    @property
    def board_info(self):
        "General board info"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.board_info_area:
            return {
                "manufacturer": str(self.fru_inventory.board_info_area.manufacturer),
                "product_name": str(self.fru_inventory.board_info_area.product_name),
                "serial_number": str(self.fru_inventory.board_info_area.serial_number),
                "part_number": str(self.fru_inventory.board_info_area.part_number),
                "fru_file_id": str(self.fru_inventory.board_info_area.fru_file_id)}
        return None

    @property
    def product_info(self):
        "General product info"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.product_info_area:
            return{
                "manufacturer": str(self.fru_inventory.product_info_area.manufacturer),
                "name": str(self.fru_inventory.product_info_area.name),
                "part_number": str(self.fru_inventory.product_info_area.part_number),
                "version": str(self.fru_inventory.product_info_area.version),
                "serial_number": str(self.fru_inventory.product_info_area.serial_number),
                "asset_tag": str(self.fru_inventory.product_info_area.asset_tag)}
        return None

    @property
    def component_info(self):
        "Method which fetches data about fru devices utilizing ipmitool"

        try:
            proc = subprocess.run(
                [f'ipmitool'] + self._ipmitool_baseargs + ['fru', 'print'], encoding='utf-8', stdout=subprocess.PIPE
            )
            if proc.returncode != 1:  # This is a weird check, because ipmitool fails the program even if there is no apparent reason for it
                proc.check_returncode()
            return dictonarify_output(proc.stdout)
        except CalledProcessError as cp_err:
            log.error(f'Ipmitool failed, exit code: {cp_err.returncode}')
            log.error(f'Process output: {cp_err.output}')

    def aggregate(self):
        "Method which aggregates all of the sub-info into one dictionary for scraping purposes"
        return {
            'system_components': self.component_info,
            'product_info': self.product_info,
            'board_info': self.board_info
        }


def dictonarify_output(output_str):
    "Function which parses output into sepearate component strings"
    components = []
    component = ''
    for line in output_str.split('\n'):
        line = line.strip()
        if not line:  # Empty line signifies next component incoming
            if component.strip():  # Check for an empty object
                components.append(f'{component}\n')
            component = ''
        else:
            component += f'{line}\n'
    return list(filter(None, [dictonarify(component) for component in components]))


def dictonarify(component):
    "Function which parses components into dictionaries"
    lines = component.split('\n')  # First line is always header
    k, v = [header_val.strip() for header_val in lines[0].split(':')]
    fru_name, fru_id = re.fullmatch(FRU.COMPONENT_HEADER_REGEXP, v).groups()
    try:
        # Decoding properties
        properties = {}
        for line in filter(lambda x: x != '', lines[1:]):  # We need to filter out blank lines
            k, v = re.fullmatch(FRU.PROPERTY_LINE_REGEXP, line).groups()
            if k != FRU.BOARD_EXTRA:  # Skipping board-extra thingy
                properties[k] = v

        result = {
            k: fru_name,
            'fru_id': fru_id,
            'properties': properties
        }
    except AttributeError:
        log.debug(f'Decoded a FRU entity which is not present in the system, skipping it: {lines[0]}')
        return None
    return result


class FRUChassis(FRUInventoryOwner):
    "Class for accessing fru chassis data "

    def fru_chassis_info(self):
        "Chassis info. Type field meaning can be found in pyipmi/fru.py"
        if not self.fru_inventory:
            self._fetch_inventory()
        if self.fru_inventory.chassis_info_area:
            return {
                "type": CHASSIS_MAP.get(self.fru_inventory.chassis_info_area.type, 'undefined'),
                "part_number": str(self.fru_inventory.chassis_info_area.part_number).strip(),
                "serial_number": str(self.fru_inventory.chassis_info_area.serial_number).strip()
            }
        return None
