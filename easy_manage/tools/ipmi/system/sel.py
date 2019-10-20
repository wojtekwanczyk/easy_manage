"TODO: Implement Event type and content parsing"
import logging
from pyipmi.sel import SelEntry
from pyipmi.event import EVENT_ASSERTION, EVENT_DEASSERTION
from easy_manage.tools.ipmi.system.sdr_maps import SENSOR_TYPE_MAP
from easy_manage.tools.ipmi.system.event_maps import EVENT_TYPE_MAP
from easy_manage.tools.ipmi.system.typecodes import TYPECODES, SENSOR_SPECIFIC, SEN_SPEC_EXT_FUNC
from easy_manage.tools.ipmi.system.reading_kind import get_reading_kind, ReadingKind

log = logging.getLogger(__name__)


class SEL:
    "Class for fetching SEL data records"

    def __init__(self, ipmi):
        self._ipmi = ipmi
        self.threshold_events_list = None
        self.discrete_events_list = None
        self.all_events = None

    def _fetch_system_event_list(self):
        "Fetches all SEL SYSTEM events entries"
        entries = self._ipmi.get_sel_entries()

        def is_system_event(event):
            return event.type == SelEntry.TYPE_SYSTEM_EVENT

        sys_events = list(filter(is_system_event, entries))
        # Filter events to those which are compliant with IPMI v2.0 formatting

        def is_compliant(event):
            return event.evm_rev == 0x04

        self.all_events = list(filter(is_compliant, sys_events))

    def _parse_all_events(self):
        "Parses all events and divides them into 2 categories: Threshold and Discrete"
        if not self.all_events:
            self._fetch_system_event_list()
        self.threshold_events_list = list(
            map(ThresholdEvent, filter(ThresholdEvent.is_threshold, self.all_events))
        )
        self.discrete_events_list = list(
            map(DiscreteEvent, filter(DiscreteEvent.is_discrete, self.all_events))
        )

    def threshold_events(self):
        "Returns list of filtered threshold events"
        self._parse_all_events()
        return self.threshold_events_list

    def discrete_events(self):
        "Returns list of filtered discrete events"
        self._parse_all_events()
        return self.discrete_events_list


class AbstractEvent:
    "Class which includes all of the common elements in events"
    ASSERTION = EVENT_ASSERTION
    DEASSERTION = EVENT_DEASSERTION
    BYTE_CONTENT_ABSENT = 0b00
    BYTE_CONTENT_OEM = 0b10
    BYTE_CONTENT_SENSOR_SPECIFIC = 0b11
    BYTE_UNSPECIFIED = 0xFF

    DATA_UNSPECIFIED = 0xF
    EVENT_EXTENSION_CODE = 0b11

    def __init__(self, event):
        self._event = event
        self._is_sensor_specific = False
        self._val_map = None
        self._sensor_type = self._event.sensor_type
        self.reading_kind = get_reading_kind(event.event_type)
        self._initialize_val_map(event.event_type)

    # Public API
    @property
    def sensor_type(self):
        "Returns type of sensor, which generated the event"
        return SENSOR_TYPE_MAP[self._sensor_type]

    @property
    def sensor_nr(self):
        "Return sensor's number, which generated the event"
        return self._event.sensor_number

    @property
    def name(self):
        "Returns sensor description string"
        return str(self._event)

    @property
    def timestamp(self):
        "Returns timestamp of the event"
        # TODO: Maybe parse it, and check out it's format
        return self._event.timestamp

    @property
    def direction(self):
        "Tells if event was asserted or deasserted, whatever the f.. it means"
        direction = self._event.event_direction
        if direction is AbstractEvent.ASSERTION:
            return "assertion"
        if direction is AbstractEvent.DEASSERTION:
            return "deassertion"
        return "unrecognised"

    @property
    def data(self):
        "Abstract method for threshold and discrete event to implement"
        # TODO: Make this method be utilized in subclasses, so only decoding function is passed (thus eliminating repeated code)
        raise NotImplementedError

    def _initialize_val_map(self, evt_typecode):
        evt_kind = self.reading_kind
        try:
            if evt_kind in (ReadingKind.DISCRETE, ReadingKind.THRESHOLD):
                self._val_map = TYPECODES[evt_typecode]
            elif evt_kind == ReadingKind.SENSOR_SPECIFIC:
                self._val_map = SENSOR_SPECIFIC[self._sensor_type]
                self._is_sensor_specific = True
            else:
                self._val_map = None
                log.error(f'No val-map matched in map for evt_kind UNSUPPORTED')
        except KeyError:
            raise NotImplementedError(
                f'No implemented val-map for evt_typecode: {hex(evt_typecode)}, reading kind: {evt_kind}'
            )

    def _parse_extension_code(self, ev_offset, fun_name, data):
        try:
            return (
                SEN_SPEC_EXT_FUNC[self._sensor_type][
                    ev_offset
                ][fun_name](data)
            )
        except KeyError as k_err:
            log.error(
                f'Method {fun_name} not implemented for sensor_type: {hex(self._sensor_type).upper()}, val-map: {self._val_map}'
            )
            log.exception(k_err)
            return None

    def _parse_extension_codes(self, data_dict, offset, dat_2_tuple, dat_3_tuple):
        dat_2_cont, data_2 = dat_2_tuple
        dat_3_cont, data_3 = dat_3_tuple
        if dat_2_cont is AbstractEvent.EVENT_EXTENSION_CODE:
            evt_extension = self._parse_extension_code(
                offset, 'parse_ext_2', data_2)
            data_dict["event_extensions"].append(evt_extension)

        if dat_3_cont is AbstractEvent.EVENT_EXTENSION_CODE:
            evt_extension = self._parse_extension_code(
                offset, 'parse_ext_3', data_3)
            data_dict["event_extensions"].append(evt_extension)


class ThresholdEvent(AbstractEvent):
    "Class for events which are threshold-based"
    THRESHOLD_EVENT_TYPE = 0x01
    # Second byte
    BYTE_TRIGGER_READING = 0b01
    # Third byte
    BYTE_THRESHOLD_VALUE = 0b01

    @staticmethod
    def is_threshold(event):
        "Returns boolean based on SelEvent object"
        return event.event_type == ThresholdEvent.THRESHOLD_EVENT_TYPE

    @property
    def data(self):
        "Returns all of the event's essential data"
        data_dict = {"event_extensions": []}
        data_1, data_2, data_3 = self._event.event_data
        data_dict["direction"] = self.direction

        # Decoding of byte 1
        offset = data_1 & 0x0F

        if self.reading_kind is ReadingKind.SENSOR_SPECIFIC:
            raise RuntimeError(
                f'Encountered discrete reading class ({self.reading_kind}) in threshold sensor! sen_type: {self.sensor_type}'
            )
        data_dict["value"] = self._val_map[offset]

        # Bytes 2 and 3 are optional
        if data_2 is not AbstractEvent.DATA_UNSPECIFIED and data_3 is not AbstractEvent.DATA_UNSPECIFIED:
            self._decode_event_extension(data_dict, offset ,data_1, data_2, data_3)
        return data_dict

    def _decode_event_extension(self, data_dict, offset, data_1, data_2, data_3):
        dat_2_cont = (data_1 & 0xC0) >> 6
        dat_3_cont = (data_1 & 0x30) >> 4
        # Further decoding relies on prescence of bytes 2 and 3 of event data
        if dat_2_cont is ThresholdEvent.BYTE_TRIGGER_READING:
            data_dict["trigger_reading"] = data_2
        if dat_3_cont is ThresholdEvent.BYTE_THRESHOLD_VALUE:
            data_dict["threshold_value"] = data_3

        self._parse_extension_codes(data_dict, offset, (dat_2_cont, data_2), (dat_3_cont, data_3))


class DiscreteEvent(AbstractEvent):
    "Class for events which are discrete-based"
    DISCRETE_EVENT_TYPE_RANGE = list(range(0x02, 0xD))
    SENSOR_SPECIFIC_CODE = 0x6F
    # Second byte
    BYTE_PREVIOUS_STATE = 0b01
    # Third byte
    BYTE_RESERVED = 0b01
    @staticmethod
    def is_discrete(event):
        "Returns boolean based on SelEvent object"
        return event.event_type in DiscreteEvent.DISCRETE_EVENT_TYPE_RANGE or event.event_type == DiscreteEvent.SENSOR_SPECIFIC_CODE

    @property
    def data(self):
        data_1, data_2, data_3 = self._event.event_data
        data_dict = {"event_extensions": []}
        # Decoding of byte 1
        offset = data_1 & 0x0F

        data_dict["direction"] = self.direction
        data_dict["value"] = self._val_map[offset]

        if data_2 is not AbstractEvent.DATA_UNSPECIFIED and data_3 is not AbstractEvent.DATA_UNSPECIFIED:
            self._decode_event_extension(data_dict, offset, data_1, data_2, data_3)
        return data_dict

    def _decode_event_extension(self, data_dict, offset, data_1, data_2, data_3):
        dat_2_cont = (data_1 & 0xC0) >> 6
        dat_3_cont = (data_1 & 0x30) >> 4
        if (dat_2_cont is DiscreteEvent.BYTE_PREVIOUS_STATE) and (data_3 is not AbstractEvent.BYTE_UNSPECIFIED):
            severity_offset = data_2 & 0x0F
            prev_reading_type_offset = (data_2 & 0xF0) >> 4

            if prev_reading_type_offset is not AbstractEvent.BYTE_UNSPECIFIED:  # Parsing of previous reading
                if self.reading_kind is ReadingKind.SENSOR_SPECIFIC:
                    valmap = SENSOR_SPECIFIC[self._sensor_type]
                else:
                    valmap = TYPECODES[self._event.event_type]
                data_dict["previous_state"] = valmap[prev_reading_type_offset]

            if severity_offset is not AbstractEvent.BYTE_UNSPECIFIED:  # Parsing of severity of the event
                data_dict["severity"] = TYPECODES[0x7][severity_offset]

        self._parse_extension_codes(data_dict, offset, (dat_2_cont, data_2), (dat_3_cont, data_3))
