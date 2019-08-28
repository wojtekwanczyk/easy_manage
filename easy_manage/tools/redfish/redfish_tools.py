"Module containing useful methods to simplify communication with Devices using Redfish Standard"

import logging
import operator
from datetime import datetime
from easy_manage.utils import utils


LOGGER = logging.getLogger('RedfishConnector')
LOGGER.setLevel(logging.INFO)

class RedfishTools:
    "Class with useful methods to simplify communication with Devices using Redfish Standard"

    def __init__(self):
        self.endpoint = None
        self.name = None
        self.data = None
        self.last_update = None
        self.db = {}
        self.db_filter = None
        self.db_collection = None
        self.connector = None
        self.client = None
        self.db_filter_name = None
        self.force_fetch = None

    def set_force_fetch(self, value):
        """When value is set, _fetch() method always get latest data from Redfish.
        Such approach is not advisable and could overload Redfish Controller"""
        self.force_fetch = value

    def _fetch(self, level=1, interval=60, force=False):
        """Fetches data from device through Redfish interface and passes it to database.
        If the session has not been established, then data is fetched from database. When
        data has been fetched from Redfish Connector in less than `interval` seconds, it won't
        be fetched once again
        :param level: How recursively deep data should be fetched from Redfish
        :param interval: Minimal time in seconds between two Redfish fetch requests
        :param force: If set, method ignores interval parameter and forces fetch from Redfish
        :return: Dictionary with fetched data (copy of self.data)"""
        force = self.force_fetch if self.force_fetch else force
        interval_bool = self.last_update and (datetime.now() - self.last_update).seconds > interval
        if self.connector.connected and (force or (not self.last_update or interval_bool)):
            # fetch through redfish
            LOGGER.info("Fetching data from BMC")
            self.data = self._update_recurse(self.endpoint, level)
            for key, value in self.data.items():
                if key.startswith('/redfish'):
                    self.data = value
                    break
            self.last_update = datetime.now()
        else:
            LOGGER.info("Fetching data from memory")
        return self.data

    def _save_to_db(self):
        "DEPRECATED - Save data to database"
        self.data.update(self.db_filter)
        self.db[self.db_collection].update(
            self.db_filter,
            self.data,
            upsert=True)

    def _fetch_from_db(self):
        "DEPRECATED - Fetch data from database"
        self.data = self.db[self.db_collection].find_one(self.db_filter)

    def get_data(self, endpoint):
        """Get data from endpoint. Wrapper for redfish client"""
        resp = self.connector.client.get(endpoint)
        return resp.dict

    def _search_recurse(self, name, structure=None, i=0):
        """
        Searches for `name` iterable object
        :param name: Name to search
        :param structure: Iterable structure to search in
        :param all_data: Common list with all collected pairs
        (key, value) passed through all levels of recursion
        :param i: just for debugging
        :return: List with all collected pairs
        (key, value) containing `name`
        """
        tuple_list = []

        if isinstance(structure, dict):
            for key, value in structure.items():
                if utils.is_iterable(value):
                    tuples = self._search_recurse(name, value, i + 1)
                    if tuples:
                        prefixed_tuples = utils.prefix_tuples(key, tuples)
                        tuple_list += prefixed_tuples
                if name in (key, value):
                    tuple_list.append((key, value))
        elif isinstance(structure, list):
            for elem in structure:
                tuple_list += self._search_recurse(name, elem, i + 1)
        return tuple_list

    def _find_all(self, name):
        """
        Finds `name` in data stored locally retrieved
        earlier from Redfish connector
        :param name: Name to search
        :return: List of tuples containing info about found
        value and its parent
        """
        found = []
        for endpoint, data in self.data.items():
            # print(endpoint)  # print searched endpoints
            element_list = self._search_recurse(name, data)
            if element_list:
                prefixed_tuples = utils.prefix_tuples(endpoint, element_list)
                found += prefixed_tuples
        return found

    def _find(self, name_list, strict=False, data=None, misses=5, force_fetch=False):
        """
        Finds a field with a "dictionary path" which includes
        all entries in `name_list` in provided data dictionary or
        data fetched from Redfish controller.
        :param name_list: List of names in "dictionary path"
        :return: Single object under last entry in name_list
        """
        if strict:
            in_or_eq = operator.eq
        else:
            in_or_eq = operator.contains

        # starting point - default argument
        if data is None or force_fetch:
            data = self._fetch(force=force_fetch)

        # all names in list have been found
        if not name_list:
            return data

        # data is a list - CAUTION!!! - not sure if works
        if data is list:
            for entry in data:
                found = self._find(name_list, strict, entry, misses)
                if found:
                    return found

        # we went too deep or cannot iterate over data
        if (not misses and name_list) or not isinstance(data, dict):
            return None

        to_find = name_list[0]
        found = None
        for key, value in data.items():
            if in_or_eq(key, to_find):
                found = self._find(name_list[1:], strict, value, misses)
            else:
                found = self._find(name_list, strict, value, misses-1)
            if found:
                return found

        return None

    def _update_recurse(self, endpoint=None, max_depth=3, data=None):
        """
        Update data about remote system
        :param endpoint: Endpoint from which recursive update starts
        :param max_depth: Maximum depth for recursive update. This
        parameter is essential to prevent reference loop
        :param data: Common dictionary which stores collected data on all
        levels of recursion
        :return: Dictionary with endpoints as keys and fresh data stored
        beneath such endpoint as dictionary value
        """
        if not endpoint:
            endpoint = self.endpoint
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
        if not data:
            data = {}
        # LOGGER.info(f"Updating data from {endpoint} with depth {max_depth}")
        if max_depth == 0 or endpoint in data.keys():
            return data
        print(endpoint)
        resp = self.get_data(endpoint)
        data[endpoint] = resp
        if isinstance(resp, dict):
            for key, value in resp.items():
                if key == '@odata.id':
                    if value == endpoint:
                        continue
                    data = self._update_recurse(value, max_depth - 1, data)
                if utils.is_iterable(value):
                    endpoints = RedfishTools._endpoint_inception(value)
                    for endp in endpoints:
                        data = self._update_recurse(endp, max_depth - 1, data)
        return data

    def update_data(self):
        """
        Basically `recursive_update()` wrapper to retrieve
        whole data from Redfish connector
        """
        self.data = self._update_recurse(self.endpoint)
        self.last_update = datetime.now()

    @staticmethod
    def _endpoint_inception(iterable, max_depth=3, endpoints=None):
        """
        We need to go deeper. Aka extract_endpoints().
        Search for every endpoint reference stored in iterable
        (list, dict) object.
        """
        if not endpoints:
            endpoints = []
        if isinstance(iterable, list):
            for elem in iterable:
                endpoints = RedfishTools._endpoint_inception(elem, max_depth - 1, endpoints)
        if isinstance(iterable, dict):
            for key, value in iterable.items():
                if utils.is_iterable(value):
                    endpoints = RedfishTools._endpoint_inception(
                        value,
                        max_depth - 1,
                        endpoints)
                elif key == '@odata.id':
                    endp = value.split('#')[0]
                    if endp not in endpoints:
                        endpoints.append(endp)
        return endpoints

    def _parse_odata(self, odata_iterable):
        """
        Exchange useless @odata keys in a dictionary
        for more readable keys
        """
        if not odata_iterable:
            return None
        parsed_dict = dict()
        if isinstance(odata_iterable, list):
            for index, elem in enumerate(odata_iterable):
                if isinstance(elem, tuple):
                    parsed_dict[elem[0]] = elem[1]['@odata.id']
                else:
                    parsed_dict[index] = elem['@odata.id']
        else:
            for key, value in odata_iterable.items():
                if key == '@odata.id':
                    parsed_dict[value] = self.get_data(value)
                else:
                    parsed_dict[key] = value['@odata.id']
        return parsed_dict

    @staticmethod
    def remove_odata(data):
        "Removes all odata entries"
        new_data = {}
        for key, value in data.items():
            if 'odata' not in key:
                new_data[key] = value
        return new_data

    def _get_dict_containing(self, name, data=None, misses=5):
        """
        finds a dictionary containing 'name' as key or value in data
        stored locally retrieved earlier from Redfish connector
        :param name: name to search in 'self.data'
        :return: dictionary containing name as key or value
        """

        # starting point - default argument
        if data is None:
            data = self.data

        # we went too deep or cannot iterate over data
        if not misses or not utils.is_iterable(data):
            return None

        found = None

        # iterate over list and check them
        if isinstance(data, list):
            for elem in data:
                found = self._get_dict_containing(name, elem, misses)
                if found:
                    return found
            return None

        # such element is in this dictionary
        for key, value in data.items():
            if name in key or name in value:
                return data

        # if not found in current dictionary, we search through curent dict values
        for value in data.values():
            found = self._get_dict_containing(name, value, misses-1)
            if found:
                return found

        return None

    def _get_basic_info(self, data=None):
        self._fetch()
        return_data = {}
        if not data:
            data = self.data
        for key, value in data.items():
            if not utils.is_iterable(value):
                return_data[key] = value
        return self.remove_odata(return_data)

    def evaluate_endpoints(self, endpoints):
        "Returns dictionary with endpoints' data as values"
        data = {}
        for endpoint in endpoints:
            data[endpoint] = self.get_data(endpoint)
        return data

    def _get_device_info(self, name, level=2):
        "Get device info from Redfish Links"
        endpoints = self._endpoint_inception(self._find([name]), level)
        return self.evaluate_endpoints(endpoints)
