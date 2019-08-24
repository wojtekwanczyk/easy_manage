"SDR Repository IPMI commands and utilities Module"
from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon
from pyipmi.errors import DecodingError
from .sdr_maps import SENSOR_TYPE_MAP, RATE_UNIT_MAP, UNIT_MAP, map_code_to_value
from easy_manage.tools.ipmi.system.typecodes import TYPECODES
SDR_TYPE_FULL_SENSOR_RECORD = 0x01
SDR_TYPE_COMPACT_SENSOR_RECORD = 0x02
THRESHOLD_SENSOR_CODE = 0x01
DISCRETE_SENSOR_RANGE = list(range(0x02, 0x70))
COMPACT_RECORD_TYPE = 0x02
FULL_RECORD_TYPE = 0x01


def parse_repository_info(repository):
    """ Function which parses returned object into a dictionary of entries"""
    return {
        "sdr_version": repository.sdr_version,
        "record_count": repository.record_count,
        "free_space": repository.free_space,
        "most_recent_addition": repository.most_recent_addition
    }


class AbstractSDR:
    "Superclass for SDR's, contains common elements"

    def __init__(self, sdr_object):
        self._sdr_object = sdr_object
        # Only full and compact SDR are supported
        self._value_map = None

        evt_reading_typecode = sdr_object.event_reading_type_code
        kind = AbstractSDR.get_sensor_kind(evt_reading_typecode)
        if kind in ('discrete', 'threshold'):
            # Value map is specified only for threshold and discrete sensors
            self._value_map = TYPECODES[evt_reading_typecode]
    # Static methods
    @staticmethod
    def get_sdr_object(sdr):
        "Creates SDR object of proper type based on library SDR object"
        ret_sdr = None
        sdr_type = sdr.get_type()
        if sdr_type == FULL_RECORD_TYPE:
            ret_sdr = FullSDR(sdr)
        elif sdr_type == COMPACT_RECORD_TYPE:
            ret_sdr = CompactSDR(sdr)
        return ret_sdr

    @staticmethod
    def get_sensor_kind(reading_code):
        "Returns sensor class based on given sensor code"
        if reading_code == THRESHOLD_SENSOR_CODE:
            return 'threshold'
        if reading_code in DISCRETE_SENSOR_RANGE:
            return 'discrete'
        return 'other'
    # Public API
    # Abstract methods to override in child classes

    def sdr_sensor_capabilities(self):
        "Returns sensor's capabilities dict"
        raise NotImplementedError

    def parse_sensor_reading(self, raw_value):
        "Abstract method for parsing raw reading into a value"
        raise NotImplementedError

    def sdr_sensor_unit(self):
        "Returns dict with unit info"
        raise NotImplementedError

    # Common getters
    def sdr_sensor_kind(self):
        "Returns sensor class based on stored sdr object's instance"
        reading_code = self._sdr_object.event_reading_type_code
        return AbstractSDR.get_sensor_kind(reading_code)

    def sdr_type(self):
        "Returns SDR type in hex"
        return self._sdr_object.type

    def sdr_sensor_type(self):
        "Returns string with sensor type"
        return map_code_to_value(
            self._sdr_object.sensor_type_code, SENSOR_TYPE_MAP)

    def sdr_name(self):
        "Returns SDR string, parsed from record"
        return self._sdr_object.device_id_string

    def sdr_record_key(self):
        "Returns record key for unique identificaiton of monitored sensor"
        return {
            "owner_id": self._sdr_object.owner_id,
            "fru_owner_lun":  self._sdr_object.owner_lun,
            "sensor_number": self._sdr_object.number
        }

    # TODO: Implement Monitored entity type and ID, if we have the time to do so


class FullSDR(AbstractSDR):
    "Class which represents 8 bit sensor with thresholds data record"
    # public API

    def parse_sensor_reading(self, raw_value):
        "Parses full SDR sensor reading, provided raw value"
        # TODO: Check if thresholds are being used in analog (normal) sensors
        if self.sdr_sensor_kind() not in ('discrete', 'threshold'):
            return self._sdr_object.convert_sensor_raw_to_value(raw_value)
        try:
            return self._value_map[raw_value]
        except KeyError:
            print(
                "Key error encountered, raw value cannot be parsed by this SDR object")
            return None

    def sdr_sensor_capabilities(self):
        "Returns sensor's capabilities"
        return self._sdr_object.capabilities

    def sdr_sensor_unit(self):
        "Returns unit information of the sensor"
        return {
            'base_unit': map_code_to_value(self._sdr_object.units_2, UNIT_MAP),
            'rate_unit': map_code_to_value(
                self._sdr_object.rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[self._sdr_object.percentage]
        }

    # Public API
    def sdr_sensor_bounds(self):
        "Returns sensor readings max/mins with their respective values"
        return {
            "normal_maximum":  self._sdr_object.normal_maximum,
            "normal_minimum":  self._sdr_object.normal_minimum,
            "sensor_maximum_reading":  self._sdr_object.sensor_maximum_reading,
            "sensor_minimum_reading":  self._sdr_object.sensor_minimum_reading
        }

    def sdr_sensor_thresholds(self):
        "Returns sensor thresolds dictionary"
        return self._sdr_object.threshold


class CompactSDR(AbstractSDR):
    "Class which represents compact sensor data record"

    def parse_sensor_reading(self, raw_value):
        "Parses compact SDR sensor reading, provided raw value"
        try:
            return self._value_map[raw_value]
        except KeyError:
            print("Key error encountered, raw value cannot be parsed by this SDR object")
            return None

    def sdr_sensor_capabilities(self):
        "Method which decodes sensor's capabilities based on given info byte"
        capabilities_byte = self._sdr_object.capabilities
        capabilities = []

        # ignore sensor
        if capabilities_byte & 0x80:
            capabilities.append('ignore_sensor')
        # sensor auto re-arm support
        if capabilities_byte & 0x40:
            capabilities.append('auto_rearm')
        # sensor hysteresis support
        HYSTERESIS_MASK = 0x30
        HYSTERESIS_IS_NOT_SUPPORTED = 0x00
        HYSTERESIS_IS_READABLE = 0x10
        HYSTERESIS_IS_READ_AND_SETTABLE = 0x20
        HYSTERESIS_IS_FIXED = 0x30
        if capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_NOT_SUPPORTED:
            capabilities.append('hysteresis_not_supported')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_READABLE:
            capabilities.append('hysteresis_readable')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_READ_AND_SETTABLE:
            capabilities.append('hysteresis_read_and_setable')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_FIXED:
            capabilities.append('hysteresis_fixed')
        # sensor threshold support
        THRESHOLD_MASK = 0x0C
        THRESHOLD_IS_NOT_SUPPORTED = 0x00
        THRESHOLD_IS_READABLE = 0x08
        THRESHOLD_IS_READ_AND_SETTABLE = 0x04
        THRESHOLD_IS_FIXED = 0x0C
        if capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_NOT_SUPPORTED:
            capabilities.append('threshold_not_supported')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_READABLE:
            capabilities.append('threshold_readable')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_READ_AND_SETTABLE:
            capabilities.append('threshold_read_and_setable')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_FIXED:
            capabilities.append('threshold_fixed')
        return capabilities

    def sdr_sensor_unit(self):
        "Returns unit information of the sensor"
        rate_unit = (self._sdr_object.units_1 >> 3) >> 0x7
        percentage = self._sdr_object.units_1 & 0x1
        return {
            'base_unit': map_code_to_value(self._sdr_object.units_2, UNIT_MAP),
            'rate_unit': map_code_to_value(rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[percentage]
        }


class SDRRepository:
    """ Class for dealing with retrieving the IPMI SDR Repository data"""

    def __init__(self, ipmi):
        self._ipmi = ipmi
        self._repo_info = None
        self._sdrs = None

    def fetch_sdr_object_list(self):
        """ Returns list of SDR objects"""

        repo = self._ipmi.get_sdr_repository_info()
        repo = parse_repository_info(repo)
        if self._is_stale(repo) or self._sdrs is None:
            sdrs = self._fetch_sdrs()
        else:
            sdrs = self._sdrs
        unfiltered = list(map(AbstractSDR.get_sdr_object, sdrs))
        def isNone(x): return x is not None
        filtered = list(filter(isNone, unfiltered))
        self._sdrs = filtered
        return filtered

    def fetch_repository_info(self):
        """ Fetches and saves the data in the object"""
        if not self._repo_info:
            repo = self._ipmi.get_sdr_repository_info()
            self._repo_info = parse_repository_info(repo)
        return self._repo_info

    def _fetch_sdrs(self):
        """ Fetches SDR entries from the BMC"""
        tmp_sdrs = self._get_repository_sdr_list()
        self._sdrs = list(filter(lambda x: (x is not None), tmp_sdrs))
        return self._sdrs

    def _get_repository_sdr(self, record_id, reservation_id=None):
        """ Method for fetching a single record, and next record's ID in a tuple"""
        (next_id, record_data) = get_sdr_data_helper(
            self._ipmi.reserve_sdr_repository, self._ipmi._get_sdr_chunk,
            record_id, reservation_id)
        try:
            return (SdrCommon.from_data(record_data, next_id), next_id)
        except DecodingError as ex:
            print(ex)
            # By policy, we skip unsupported records
            return (None, next_id)

    def _sdr_repository_entries(self):
        """ Generator of tuples (next_id, entry)"""
        reservation_id = self._ipmi.reserve_sdr_repository()
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
        curr = self._repo_info
        if curr is None or curr["most_recent_addition"] != new_info["most_recent_addition"]:
            return True
        return False
