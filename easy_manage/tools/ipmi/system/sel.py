"TODO: Implement Event type and content parsing"
from pyipmi.sel import SelEntry
from pyipmi.event import EVENT_ASSERTION, EVENT_DEASSERTION
from easy_manage.tools.ipmi.system.sdr_maps import SENSOR_TYPE_MAP
from easy_manage.tools.ipmi.system.event_maps import EVENT_TYPE_MAP
from easy_manage.tools.ipmi.system.typecodes import TYPECODES

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
            filter(ThresholdEvent.is_threshold, self.all_events)
        )
        self.discrete_events_list = list(
            filter(DiscreteEvent.is_discrete, self.all_events)
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
    def __init__(self, event):
        self._event = event
        self.data = event.data

    # Public API
    @property
    def sensor_type(self):
        "Returns type of sensor, which generated the event"
        return SENSOR_TYPE_MAP[self._event.sensor_type]

    @property
    def name(self):
        "Returns sensor description string"
        return str(self._event)

    @property
    def sensor_nr(self):
        "Return sensor's number, which generated the event"
        return self._event.sensor_number

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
    def event_type(self):
        "Returns event type based on given info"
        return EVENT_TYPE_MAP[self._event.event_type]

    @property
    def data(self):
        "Abstract method for threshold and discrete event to implement"
        raise NotImplementedError


class ThresholdEvent(AbstractEvent):
    "Class for events which are threshold-based"
    THRESHOLD_EVENT_TYPE = 0x01
    # Second byte
    BYTE_TRIGGER_READING = 0b01
    # Third byte
    BYTE_TRIGGER_VALUE = 0b01
    # Shared
    EVENT_EXTENSION_CODE = 0b11

    @staticmethod
    def is_threshold(event):
        "Returns boolean based on SelEvent object"
        return event.type == ThresholdEvent.THRESHOLD_EVENT_TYPE

    @property
    def data(self):
        data = {"event_extension": []}
        data_1, data_2, data_3 = self._event.event_data
        # Decoding of byte 1
        offset = data_1 & 0x0F
        dat_2_cont = (data_1 & 0xC0) >> 4
        dat_3_cont = (data_1 & 0x30) >> 4

        data["value"] = EVENT_TYPE_MAP[self._event.type].offsets[offset].value

        if dat_2_cont is ThresholdEvent.BYTE_TRIGGER_READING:
            data["reading"] = data_2

        if dat_3_cont is ThresholdEvent.BYTE_TRIGGER_VALUE:
            data["threshold_value"] = data_3

        if dat_2_cont is ThresholdEvent.EVENT_EXTENSION_CODE:
            ext_code_2 = (
                EVENT_TYPE_MAP[self._event.sensor_type]
                .offsets[offset]
                .parse_ext_2(dat_2_cont)
            )
            data["event_extension"].append(ext_code_2)

        if dat_3_cont is ThresholdEvent.EVENT_EXTENSION_CODE:
            ext_code_3 = (
                EVENT_TYPE_MAP[self._event.sensor_type]
                .offsets[offset]
                .parse_ext_3(dat_3_cont)
            )
            data["event_extension"].append(ext_code_3)
        return data


class DiscreteEvent(AbstractEvent):
    "Class for events which are discrete-based"
    DISCRETE_EVENT_TYPE_RANGE = list(range(0x02, 0x70))
    # Second byte
    BYTE_PREVIOUS_STATE = 0b01
    # Third byte
    BYTE_RESERVED = 0b01

    @staticmethod
    def is_discrete(event):
        "Returns boolean based on SelEvent object"
        return event.type in DiscreteEvent.DISCRETE_EVENT_TYPE_RANGE

    @property
    def data(self):
        data = {"event_extension": []}
        data_1, data_2, data_3 = self._event.event_data
        # Decoding of byte 1
        offset = data_1 & 0x0F
        dat_2_cont = (data_1 & 0xC0) >> 4
        dat_3_cont = (data_1 & 0x30) >> 4
        data["value"] = EVENT_TYPE_MAP[self._event.sensor_type].offsets[offset].value
        if (dat_2_cont is DiscreteEvent.BYTE_PREVIOUS_STATE) and (data_3 is not AbstractEvent.BYTE_UNSPECIFIED):
            severity_offset = data_2 & 0x0F
            prev_reading_type_offset = (data_2 & 0xF0) >> 4
            data["previous_state"] = EVENT_TYPE_MAP[self._event.sensor_type].offsets[prev_reading_type_offset]
            data["severity"] = TYPECODES[self._event.type][severity_offset]
            
        if dat_2_cont is ThresholdEvent.EVENT_EXTENSION_CODE:
            ext_code_2 = (
                EVENT_TYPE_MAP[self._event.sensor_type]
                .offsets[offset]
                .parse_ext_2(dat_2_cont)
            )
            data["event_extension"].append(ext_code_2)
        if dat_3_cont is ThresholdEvent.EVENT_EXTENSION_CODE:
            ext_code_3 = (
                EVENT_TYPE_MAP[self._event.sensor_type]
                .offsets[offset]
                .parse_ext_3(dat_3_cont)
            )
            data["event_extension"].append(ext_code_3)
        return data
