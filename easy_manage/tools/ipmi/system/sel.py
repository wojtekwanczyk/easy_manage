"TODO: Implement Event type and content parsing"
from pyipmi.sel import SelEntry
from pyipmi.event import EVENT_ASSERTION, EVENT_DEASSERTION


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
        self.timestamp = event.timestamp
        self.description = str(event)
        self.sensor_type = event.sensor_type
        self.sensor_number = event.sensor_number
        # Direction is described by assertion/deassertion flags respectievly
        self.event_direction = event.event_direction
        # TODO: Event type and data should be decoded into more human-readable format
        self.event_type = event.event_type
        self.data = event.data


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
