"SDR Repository IPMI commands Module"
from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon
from pyipmi.errors import DecodingError


class SDR:
    """ Class for dealing with retrieving the IPMI SDR Repository data"""

    def __init__(self, ipmi):
        self.ipmi = ipmi
        self.res_number = None
        self.repo_info = None
        self.res_id = None
        self.sdrs = None

    def fetch_repository(self):
        """ Returns current SDR repository data"""
        self.repo_info = self.msg('GetSdrRepositoryInfo')
        if self.is_stale(self.repo_info):
            return self.fetch_sdrs()
        return self.sdrs

    def fetch_sdrs(self):
        """ Fetches SDR entries from the BMC"""
        tmp_sdrs = self.get_repository_sdr_list()
        self.sdrs = list(filter(lambda x: (x is not None), tmp_sdrs))
        return self.sdrs

    def get_repository_sdr(self, record_id, reservation_id=None):
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

    def sdr_repository_entries(self):
        """ Generator of tuples (next_id, entry)"""
        reservation_id = self.ipmi.reserve_sdr_repository()
        record_id = 0

        while True:
            (record, next_id) = self.get_repository_sdr(
                record_id, reservation_id)
            yield record
            if next_id == 0xffff:
                break
            record_id = next_id

    def get_repository_sdr_list(self):
        """ Utilizes generator of entries"""
        return list(self.sdr_repository_entries())

    def is_stale(self, new_info):
        """ Does object needs to re-fetch data from BMC"""
        curr = self.repo_info
        if curr is None or curr.most_recent_addition != new_info.most_recent_addition:
            return True
        return False

    def msg(self, name):
        """ Utility shorthand"""
        return self.ipmi.send_message_with_name(name)
