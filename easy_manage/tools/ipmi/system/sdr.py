"SDR Repository IPMI commands and utilities Module"
from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon
from pyipmi.errors import DecodingError
from .sdr_maps import SENSOR_TYPE_MAP, RATE_UNIT_MAP, UNIT_MAP, map_code_to_value

SDR_TYPE_FULL_SENSOR_RECORD = 0x01
SDR_TYPE_COMPACT_SENSOR_RECORD = 0x02
THRESHOLD_SENSOR_CODE = 0x01
DISCRETE_SENSOR_RANGE = list(range(0x02, 0x70))
COMPACT_RECORD_TYPE = 0x02
FULL_RECORD_TYPE = 0x01


def parse_repository_info(repository):
    """ Method parses returned object into a dictionary of entries"""
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
        self.name = sdr_object.device_id_string
        # Only full and compact SDR are supported
        self.type = sdr_object.type
        self.number = sdr_object.number
        self.lun = sdr_object.owner_lun

    @staticmethod
    def create_sdr_object(sdr):
        "Creates SDR object of proper type based on library SDR object"
        ret_sdr = None
        if sdr.type == FULL_RECORD_TYPE:
            ret_sdr = FullSDR(sdr)
        elif sdr.type == COMPACT_RECORD_TYPE:
            ret_sdr = CompactSDR(sdr)
        return ret_sdr

    @staticmethod
    def get_sensor_kind(reading_code):
        "Returns sensor class based on given sensor code"
        if reading_code == THRESHOLD_SENSOR_CODE:
            return 'threshold'
        if reading_code in DISCRETE_SENSOR_RANGE:
            return 'discrete'
        return 'unsupported'


class FullSDR(AbstractSDR):
    "Class which represents 8 bit sensor with thresholds data record"

    def __init__(self, sdr_object):
        super().__init__(sdr_object)
        self.capabilities = sdr_object.capabilities

        self.sensor_type = map_code_to_value(
            sdr_object.sensor_type_code, SENSOR_TYPE_MAP)

        reading_code = sdr_object.event_reading_type_code
        self.sensor_kind = AbstractSDR.get_sensor_kind(reading_code)

        self.thresholds = sdr_object.threshold
        self.unit = {
            'base_unit': map_code_to_value(sdr_object.units_2, UNIT_MAP),
            'rate_unit': map_code_to_value(
                sdr_object.rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[sdr_object.percentage]
        }
        self.bounds = {
            "normal_maximum":  sdr_object.normal_maximum,
            "normal_minimum":  sdr_object.normal_minimum,
            "sensor_maximum_reading":  sdr_object.sensor_maximum_reading,
            "sensor_minimum_reading":  sdr_object.sensor_minimum_reading
        }

    def parse_reading(self, raw_value):
        "Parses full SDR sensor reading, provided raw value"
        return self._sdr_object.convert_sensor_raw_to_value(raw_value)


class CompactSDR(AbstractSDR):
    "Class which represents compact sensor data record"

    def __init__(self, sdr_object):
        super().__init__(sdr_object)
        # TODO: Implement

    def parse_reading(self, raw_value):
        "Parses compact SDR sensor reading, provided raw value"
        pass
        # TODO: Implement - provide concatenated reading with value ? sth like dis


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
        unfiltered = list(map(AbstractSDR.create_sdr_object, sdrs))
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
