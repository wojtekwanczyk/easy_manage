"Module which exposes basic system event log functionalities"
import logging
from pyipmi.sel import SelEntry
from easy_manage.tools.ipmi.system.SEL.events import ThresholdEvent, DiscreteEvent
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

    @property
    def threshold_events(self):
        "Returns list of filtered threshold events"
        self._parse_all_events()
        return self.threshold_events_list

    @property
    def discrete_events(self):
        "Returns list of filtered discrete events"
        self._parse_all_events()
        return self.discrete_events_list

    def aggregate(self):
        "Returns both event lists, for aggregating purposes"
        return {
            'discrete_events': list(map(lambda evt: evt.aggregate(), self.discrete_events)),
            'threshold_events':  list(map(lambda evt: evt.aggregate(), self.threshold_events))
        }
