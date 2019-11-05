"Module containing SDR records classes"
import logging
from easy_manage.tools.ipmi.system.maps.typecodes import TYPECODES, SENSOR_SPECIFIC, THRESHOLDS
from easy_manage.tools.ipmi.system.maps.sdr_maps import SENSOR_TYPE_MAP, RATE_UNIT_MAP, UNIT_MAP, map_code_to_value
from easy_manage.tools.ipmi.system.utils.reading_kind import ReadingKind, get_reading_kind, get_reading_kind_readable

log = logging.getLogger(__name__)

SDR_TYPE_FULL_SENSOR_RECORD = 0x01
SDR_TYPE_COMPACT_SENSOR_RECORD = 0x02
THRESHOLD_SENSOR_CODE = 0x01
DISCRETE_SENSOR_RANGE = list(range(0x02, 0xD))
SENSOR_SPECIFIC_CODE = 0x6F
COMPACT_RECORD_TYPE = 0x02
FULL_RECORD_TYPE = 0x01

# sensor hysteresis support
HYSTERESIS_MASK = 0x30
HYSTERESIS_IS_NOT_SUPPORTED = 0x00
HYSTERESIS_IS_READABLE = 0x10
HYSTERESIS_IS_READ_AND_SETTABLE = 0x20
HYSTERESIS_IS_FIXED = 0x30

# sensor threshold support
THRESHOLD_MASK = 0x0C
THRESHOLD_IS_NOT_SUPPORTED = 0x00
THRESHOLD_IS_READABLE = 0x08
THRESHOLD_IS_READ_AND_SETTABLE = 0x04
THRESHOLD_IS_FIXED = 0x0C


class AbstractSDR:
    "Superclass for SDR's, contains common elements"

    def __init__(self, sdr_object):
        self._sdr_object = sdr_object
        # Only full and compact SDR are supported
        self._value_mapping = None
        evt_reading_typecode = sdr_object.event_reading_type_code
        kind = get_reading_kind(evt_reading_typecode)
        if kind in (ReadingKind.DISCRETE, ReadingKind.THRESHOLD):
            # Value map is specified only for threshold and discrete sensors
            self._value_mapping = TYPECODES[evt_reading_typecode]
        if kind == ReadingKind.SENSOR_SPECIFIC:
            # Special value map, for sensor-defined states
            self._value_mapping = SENSOR_SPECIFIC[sdr_object.sensor_type_code]
        if not self._value_mapping:
            if kind in (ReadingKind.DISCRETE, ReadingKind.THRESHOLD):
                log.error(
                    f'Could not match typecode map to evt_reading_typecode: \'{evt_reading_typecode}\' for sensor of kind {kind}'
                )
            else:
                log.error(
                    f'Could not match decoding function to sensor_type_code: \'{sdr_object.sensor_type_code}\' for sensor of kind {kind}'
                )

    # Static methods
    @staticmethod
    def get_sdr_object(sdr):
        "Creates SDR object of proper type based on library SDR object"
        ret_sdr = None
        if sdr.type == FULL_RECORD_TYPE:
            ret_sdr = FullSDR(sdr)
        elif sdr.type == COMPACT_RECORD_TYPE:
            ret_sdr = CompactSDR(sdr)
        return ret_sdr

    def _parse_discrete_reading(self, raw_reading):
        binstring = raw_reading_to_binstring(raw_reading)
        return {
            'states_asserted': self._map_binstring_to_states(binstring)
        }

    def _parse_specific_reading(self, raw_reading):
        binstring = raw_reading_to_binstring(raw_reading)
        return {
            'states_asserted': self._map_binstring_to_states(binstring)
        }

    def _parse_threshold_reading(self, raw_reading):
        return {
            'value': self._sdr_object.convert_sensor_raw_to_value(raw_reading[0]),
            'thresholds': decode_thresholds(raw_reading),
        }

    def _map_binstring_to_states(self, binstring):
        states = []
        for i, asserted in enumerate(binstring):
            if asserted == '1':
                try:
                    states.append(self._value_mapping[i])
                except KeyError as k_err:
                    log.error(
                        f"Exception on sensor type: {self.sensor_type}, kind: {self.sensor_kind}, val-map: {self._value_mapping} "
                    )
                    log.exception(k_err)
                except TypeError:
                    log.error(
                        f'Value mapping is not defined on sensor type: {self.sensor_type}, kind: {self.sensor_kind}'
                    )
        return states

    def parse_sensor_reading(self, raw_value):
        "Parses full SDR sensor reading, provided raw value"
        try:
            return {
                ReadingKind.DISCRETE: self._parse_discrete_reading,
                ReadingKind.SENSOR_SPECIFIC: self._parse_specific_reading,
                ReadingKind.THRESHOLD: self._parse_threshold_reading,
            }[self.sensor_kind](raw_value)
        except KeyError:
            raise UnsupportedOperationError("Cannot read from unsupported sensor")

    # Public API
    # Abstract methods to override in child classes
    @property
    def sensor_capabilities(self):
        "Returns sensor's capabilities dict"
        raise NotImplementedError

    @property
    def sensor_unit(self):
        "Returns dict with unit info"
        raise NotImplementedError

    # Common properties
    @property
    def sensor_kind(self):
        "Returns sensor class based on stored sdr object's instance"
        typecode = self._sdr_object.event_reading_type_code
        return get_reading_kind(typecode)

    @property
    def sensor_kind_readable(self):
        "Returns a human-readable "
        return get_reading_kind_readable(self.sensor_kind)

    @property
    def sdr_type(self):
        "Returns SDR type in hex"
        return self._sdr_object.type

    @property
    def sensor_type(self):
        "Returns string with sensor type"
        return map_code_to_value(
            self._sdr_object.sensor_type_code, SENSOR_TYPE_MAP)

    @property
    def name(self):
        "Returns SDR string, parsed from record"
        decoded = self._sdr_object.device_id_string.decode()
        return ('_').join(decoded.lower().split(' '))

    @property
    def record_key(self):
        "Returns record key for unique identificaiton of monitored sensor"
        return {
            "owner_id": self._sdr_object.owner_id,
            "fru_owner_lun":  self._sdr_object.owner_lun,
            "sensor_number": self._sdr_object.number
        }

    def aggregate(self):
        "Returns all of necessary info about the sdr itself, for data aggregating purposes"
        return {
            'record_key': self.record_key,
            'name': self.name,
            'sensor_type': self.sensor_type,
            'sensor_kind': self.sensor_kind_readable,
        }


class FullSDR(AbstractSDR):
    "Class which represents 8 bit sensor with thresholds data record"
    # Public API
    @property
    def sensor_capabilities(self):
        "Returns sensor's capabilities"
        return self._sdr_object.capabilities

    @property
    def sensor_unit(self):
        "Returns unit information of the sensor"
        return {
            'base_unit': map_code_to_value(self._sdr_object.units_2, UNIT_MAP),
            'rate_unit': map_code_to_value(self._sdr_object.rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[self._sdr_object.percentage]
        }

    # Public API
    @property
    def sensor_bounds(self):
        "Returns sensor readings max/mins with their respective values"
        return {
            "normal_maximum":  self._sdr_object.normal_maximum,
            "normal_minimum":  self._sdr_object.normal_minimum,
            "sensor_maximum_reading":  self._sdr_object.sensor_maximum_reading,
            "sensor_minimum_reading":  self._sdr_object.sensor_minimum_reading
        }

    @property
    def sensor_thresholds(self):
        "Returns sensor thresolds dictionary"
        return self._sdr_object.threshold

    def aggregate(self):
        return {
            'sensor_capabilities': self.sensor_capabilities,
            'sensor_unit': self.sensor_unit,
            'sensor_bounds': self.sensor_bounds,
            **super().aggregate()
        }


class CompactSDR(AbstractSDR):
    "Class which represents compact sensor data record"
    @property
    def sensor_capabilities(self):
        "Method which decodes sensor's capabilities based on given info byte"
        capabilities_byte = self._sdr_object.capabilities
        capabilities = []

        # ignore sensor
        if capabilities_byte & 0x80:
            capabilities.append('ignore_sensor')
        # sensor auto re-arm support
        if capabilities_byte & 0x40:
            capabilities.append('auto_rearm')

        if capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_NOT_SUPPORTED:
            capabilities.append('hysteresis_not_supported')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_READABLE:
            capabilities.append('hysteresis_readable')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_READ_AND_SETTABLE:
            capabilities.append('hysteresis_read_and_setable')
        elif capabilities_byte & HYSTERESIS_MASK == HYSTERESIS_IS_FIXED:
            capabilities.append('hysteresis_fixed')

        if capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_NOT_SUPPORTED:
            capabilities.append('threshold_not_supported')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_READABLE:
            capabilities.append('threshold_readable')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_READ_AND_SETTABLE:
            capabilities.append('threshold_read_and_setable')
        elif capabilities_byte & THRESHOLD_MASK == THRESHOLD_IS_FIXED:
            capabilities.append('threshold_fixed')
        return capabilities

    @property
    def sensor_unit(self):
        "Returns unit information of the sensor"
        rate_unit = (self._sdr_object.units_1 >> 3) >> 0x7
        percentage = self._sdr_object.units_1 & 0x1
        return {
            'base_unit': map_code_to_value(self._sdr_object.units_2, UNIT_MAP),
            'rate_unit': map_code_to_value(rate_unit, RATE_UNIT_MAP),
            'percentage': (False, True)[percentage]
        }

    def aggregate(self):
        return {
            'sensor_capabilities': self.sensor_capabilities,
            'sensor_unit': self.sensor_unit,
            **super().aggregate()
        }


def raw_reading_to_binstring(raw_reading):
    """ Converts raw ipmi reading to binary-string states mask"""
    state_list = bin(raw_reading[1])[2:]
    state1 = state_list[8:16][::-1]
    state2 = state_list[0:8][::-1][:7]
    binstring = state1 + state2
    return binstring


def decode_thresholds(raw_reading):
    """ Decodes binary mask to proper threshold values"""
    binstring = bin(raw_reading[1])[4:]  # 2 first values ignored, 2 first of bin ignored ('0b')
    # it's backwards, to be documentation compatible i reverse it.
    binstring = binstring[::-1]
    thresholds = []
    for i, asserted in enumerate(binstring):
        if asserted == '1':
            thresholds.append(THRESHOLDS[i])
    return thresholds


class UnsupportedOperationError(Exception):
    """ Exception type for performing non-standard SDR actions """
