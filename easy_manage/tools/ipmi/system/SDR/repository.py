"SDR Repository IPMI commands and utilities Module"
import logging

from pyipmi.errors import DecodingError
from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon

from easy_manage.tools.ipmi.system.SDR.records import AbstractSDR

log = logging.getLogger(__name__)


def parse_repository_info(repository):
    """ Function which parses returned object into a dictionary of entries"""
    return {
        "sdr_version": repository.sdr_version,
        "record_count": repository.record_count,
        "free_space": repository.free_space,
        "most_recent_addition": repository.most_recent_addition
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
        filtered = list(filter(lambda x: (x is not None), unfiltered))
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
        except DecodingError:
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
