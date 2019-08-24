"TODO: Implement Event type and content parsing"
from pyipmi.sel import SelEntry
from pyipmi.event import EVENT_ASSERTION, EVENT_DEASSERTION
from easy_manage.tools.ipmi.system.sdr_maps import SENSOR_TYPE_MAP
from easy_manage.tools.ipmi.system.event_maps import EVENT_TYPE_MAP
class SEL:

    def __init__(self, ipmi):
        self._ipmi = ipmi
        self.threshold_events_list = None
        self.discrete_events_list = None
        self.all_events = None

    def _fetch_system_event_list(self):
        "Fetches all SEL SYSTEM events entries"
        entries = self._ipmi.get_sel_entries()
        def is_system_event(
            event): return event.type == SelEntry.TYPE_SYSTEM_EVENT
        sys_events = list(filter(is_system_event, entries))
        # Filter events to those which are compliant with IPMI v2.0 formatting
        def is_compliant(event): return event.evm_rev == 0x04
        self.all_events = list(filter(is_compliant, sys_events))

    def _parse_all_events(self):
        "Parses all events and divides them into 2 categories: Threshold and Discrete"
        if not self.all_events:
            self._fetch_system_event_list()
        self.threshold_events_list = list(
            filter(ThresholdEvent.is_threshold, self.all_events))
        self.discrete_events_list = list(
            filter(DiscreteEvent.is_discrete, self.all_events))

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

    def __init__(self, event):
        self._event = event
        self.data = event.data

    # Public API
    def event_sensor_type(self):
        "Returns type of sensor, which generated the event"
        return SENSOR_TYPE_MAP[self._event.sensor_type]

    def event_name(self):
        "Returns sensor description string"
        return str(self._event)

    def event_sensor_nr(self):
        "Return sensor's number, which generated the event"
        return self._event.sensor_number

    def event_timestamp(self):
        "Returns timestamp of the event"
        # TODO: Maybe parse it, and check out it's format
        return self._event.timestamp

    def event_direction(self):
        "Tells if event was asserted or deasserted, whatever the f.. it means"
        direction = self._event.event_direction
        if direction is AbstractEvent.ASSERTION:
            return 'assertion'
        if direction is AbstractEvent.DEASSERTION:
            return 'deassertion'
        return 'unrecognised'

    def event_type(self):
        "Returns event type based on given info"
        return EVENT_TYPE_MAP[self._event.event_type]
    
    def event_data(self):
        raise NotImplementedError

class ThresholdEvent(AbstractEvent):
    "Class for events which are threshold-based"
    THRESHOLD_EVENT_TYPE = 0x01

    @staticmethod
    def is_threshold(event):
        "Returns boolean based on SelEvent object"
        return event.type == ThresholdEvent.THRESHOLD_EVENT_TYPE


class DiscreteEvent(AbstractEvent):
    "Class for events which are discrete-based"
    DISCRETE_EVENT_TYPE_RANGE = list(range(0x02, 0x70))

    @staticmethod
    def is_discrete(event):
        "Returns boolean based on SelEvent object"
        return event.type in DiscreteEvent.DISCRETE_EVENT_TYPE_RANGE
