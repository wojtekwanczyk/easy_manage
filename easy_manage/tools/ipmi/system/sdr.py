from pyipmi.helper import get_sdr_data_helper
from pyipmi.sdr import SdrCommon


class SDR:
    def __init__(self, ipmi):
        self.ipmi = ipmi
        self.res_number = None
        self.repo_info = None
        self.res_id = None
        self.sdrs = None

    def fetch_repository(self):
        self.repo_info = self.msg('GetSdrRepositoryInfo')
        if self.is_stale(self.repo_info):
            return self.fetch_sdrs()
        else:
            return self.sdrs

    # Returns iterable sdr entry list
    def fetch_sdrs(self):
        tmp_sdrs = self.get_repository_sdr_list()
        not_none = lambda x: x is not None;
        self.sdrs = list(filter(not_none, tmp_sdrs))
        return self.sdrs

    def get_repository_sdr(self, record_id, reservation_id=None):
        (next_id, record_data) = get_sdr_data_helper(
            self.ipmi.reserve_sdr_repository, self.ipmi._get_sdr_chunk,
            record_id, reservation_id)
        try:
            return (SdrCommon.from_data(record_data, next_id), next_id)
        except Exception as ex:
            print(ex)
            # Skip the entry
            return (None, next_id)

    def get_repository_sdr_list(self, reservation_id=None):
        return list(self.sdr_repository_entries())

    def sdr_repository_entries(self):
        reservation_id = self.ipmi.reserve_sdr_repository()
        record_id = 0

        while True:
            (s, next_id) = self.get_repository_sdr(record_id, reservation_id)
            yield s
            if next_id == 0xffff:
                break
            record_id = next_id

    # Does object needs to re-fetch data
    def is_stale(self, new_info):
        curr = self.repo_info
        if curr is None:
            return True
        elif curr.most_recent_addition != new_info.most_recent_addition:
            return True
        return False

    # Utility shorthand
    def msg(self, name):
        return self.ipmi.send_message_with_name(name)
