"SDR Repository IPMI commands and utilities Module"
from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon
from pyipmi.errors import DecodingError


SDR_TYPE_FULL_SENSOR_RECORD = 0x01
SDR_TYPE_COMPACT_SENSOR_RECORD = 0x02
SENSOR_TYPE_MAP = {
    0x01: "temperature",
    0x02: "voltage",
    0x03: "current",
    0x04: "fan",
    0x05: "chassis_intrusion",
    0x06: "security_violation_attempt",
    0x07: "processor",
    0x08: "power_supply",
    0x09: "power_unit",
    0xA: "cooling_device",
    0xB: "other_unit_based_sensor",
    0xC: "memory",
    0xD: "drive_slot",
    0xE: "post_memory",
    0xF: "firmware_progress",
    0x10: "evt_logging_disable",
    0x11: "watchdog_1",
    0x12: "sys_event",
    0x13: "crit_interrupt",
    0x14: "button",
    0x15: "module_board",
    0x16: "microcontroller_coprocessor",
    0x17: "add_in_card",
    0x18: "chassis",
    0x19: "chipset",
    0x1A: "other_fru",
    0x1B: "cable_interconnect",
    0x1C: "terminator",
    0x1D: "system_boot",
    0x1E: "boot_error",
    0x1F: "base_os_boot",
    0x20: "os_stop",
    0x21: "slot_connector",
    0x22: "acpi_pwr_state",
    0x23: "watchdog_2",
    0x24: "platform_alert",
    0x25: "entity_presence",
    0x26: "monitor_asic",
    0x27: "lan",
    0x28: "management_sys_health",
    0x29: "battery",
    0x2A: "session_audit",
    0x2B: "ver_change",
    0x2C: "fru_state"
}
RATE_UNIT_MAP = {
    0b000: "none",
    0b001: "per uS",
    0b010: "per ms",
    0b011: "per s",
    0b100: "per min",
    0b101: "per hr",
    0b110: "per day"
}
UNIT_MAP = {
    # TODO

}
THRESHOLD_SENSOR_CODE = 0x01
DISCRETE_SENSOR_RANGE = list(range(0x02, 0x70))


def _parse_repository_info(repository):
    """ Method parses returned object into a dictionary of entries"""
    return {
        "sdr_version": repository.sdr_version,
        "record_count": repository.record_count,
        "free_space": repository.free_space,
        "most_recent_addition": repository.most_recent_addition
    }


class SDRRepository:
    """ Class for dealing with retrieving the IPMI SDR Repository data"""

    def __init__(self, ipmi):
        self.ipmi = ipmi
        self.res_number = None
        self.repo_info = None
        self.res_id = None
        self.sdrs = None

    def fetch_sdr_repository(self):
        """ Returns current SDR repository data"""

        repo = self.ipmi.get_sdr_repository_info()
        repo = _parse_repository_info(repo)
        if self._is_stale(repo) or self.sdrs is None:
            sdrs = self._fetch_sdrs()
        else:
            sdrs = self.sdrs
        # TODO: Mapping SDRS into objects

    def fetch_repository_info(self):
        """ Fetches and saves the data in the object"""
        if not self.repo_info:
            repo = self.ipmi.get_sdr_repository_info()
            self.repo_info = _parse_repository_info(repo)
        return self.repo_info

    def _fetch_sdrs(self):
        """ Fetches SDR entries from the BMC"""
        tmp_sdrs = self._get_repository_sdr_list()
        self.sdrs = list(filter(lambda x: (x is not None), tmp_sdrs))
        return self.sdrs

    def _get_repository_sdr(self, record_id, reservation_id=None):
        """ Method for fetching a single record, and next record's ID in a tuple"""
        (next_id, record_data) = get_sdr_data_helper(
            self.ipmi.reserve_sdr_repository, self.ipmi._get_sdr_chunk,
            record_id, reservation_id)
        try:
            return (SdrCommon.from_data(record_data, next_id), next_id)
        except DecodingError as ex:
            print(ex)
            # By policy, we skip unsupported records
            return (None, next_id)

    def _sdr_repository_entries(self):
        """ Generator of tuples (next_id, entry)"""
        reservation_id = self.ipmi.reserve_sdr_repository()
        record_id = 0

        while True:
            (record, next_id) = self._get_repository_sdr(
                record_id, reservation_id)
            yield record
            if next_id == 0xffff:
                break
            record_id = next_id

    def _get_repository_sdr_list(self):
        """ Utilizes generator of entries"""
        return list(self._sdr_repository_entries())

    def _is_stale(self, new_info):
        """ Does object needs to re-fetch data from BMC"""
        curr = self.repo_info
        if curr is None or curr["most_recent_addition"] != new_info["most_recent_addition"]:
            return True
        return False


class AbstactSDR:
    "Superclass for SDR's, contains common elements"

    def __init__(self, sdr_object):
        self.sdr_object = sdr_object
        self.name = sdr_object.device_id_string
        # Only full and compact SDR are supported
        self.type = sdr_object.type


class FullSDR(AbstactSDR):
    "Class which represents 8 bit sensor with thresholds data record"

    def __init__(self, sdr_object):
        super().__init__(sdr_object)
        # TODO: Decide if this is needed at all
        self.capabilities = sdr_object.capabilities

        self.sensor_type = self._map_code_to_value(
            sdr_object.sensor_type_code, SENSOR_TYPE_MAP)

        reading_code = sdr_object.event_reading_type_code
        self.sensor_kind = self._get_sensor_kind(reading_code)

        self.thresholds = sdr_object.threshold
        # TODO: Reimplement Full Record class fucking hell GOD DAMMIT FUUUUUUUUUCK, and then base unit should work

        self.unit = {
            'base_unit': self._map_code_to_value(sdr_object.units_2, UNIT_MAP),
            'rate_unit': self._map_code_to_value(
                sdr_object.rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[sdr_object.percentage]
        }
        self.bounds = {
            "normal_maximum":  sdr_object.normal_maximum,
            "normal_minimum":  sdr_object.normal_minimum,
            "sensor_maximum_reading":  sdr_object.sensor_maximum_reading,
            "sensor_minimum_reading":  sdr_object.sensor_minimum_reading
        }

    def _map_code_to_value(self, type_code, type_map):
        try:
            return type_map[type_code]
        except KeyError:
            return 'unsupported'

    def _get_sensor_kind(self, reading_code):
        if(reading_code == THRESHOLD_SENSOR_CODE):
            return 'threshold'
        elif reading_code in DISCRETE_SENSOR_RANGE:
            return 'discrete'


class CompactSDR(AbstactSDR):
    "Class which represents compact sensor data record"

    def __init__(self, sdr_object):
        super().__init__(sdr_object)
        # TODO: Implement
