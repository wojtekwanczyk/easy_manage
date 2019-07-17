"Module containing useful methods to simplify communication with Devices using Redfish Standard"

import logging
import operator
from datetime import datetime
from easy_manage import utils


LOGGER = logging.getLogger('RedfishConnector')
LOGGER.setLevel(logging.DEBUG)

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

    def fetch(self, level=1):
        """Fetches data from device through Redfish interface and passes it to database.
        If the session has not been established, then data is fetched from database"""
        if self.connector.connected:
            # fetch through redfish
            self.data = self.update_recurse(self.endpoint, level)
            self.last_update = datetime.now()
            self.__save_to_db()
        elif not self.data:
            LOGGER.info('Not connected. Fetching from database.')
            self.__fetch_from_db()

    def __save_to_db(self):
        "Save data to database"
        self.data.update(self.db_filter)
        self.db[self.db_collection].update(
            self.db_filter,
            self.data,
            upsert=True)

    def __fetch_from_db(self):
        "Fetch data from database"
        self.data = self.db[self.db_collection].find_one(self.db_filter)

    def get_data(self, endpoint):
        """Get data from endpoint. Wrapper for redfish client"""
        resp = self.connector.client.get(endpoint)
        return resp.dict

    def search_recurse(self, name, structure=None, i=0):
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
                    tuples = self.search_recurse(name, value, i + 1)
                    if tuples:
                        prefixed_tuples = utils.prefix_tuples(key, tuples)
                        tuple_list += prefixed_tuples
                if name in (key, value):
                    tuple_list.append((key, value))
        elif isinstance(structure, list):
            for elem in structure:
                tuple_list += self.search_recurse(name, elem, i + 1)
        return tuple_list

    def find_all(self, name):
        """
        Find `name` in data stored locally retrieved
        earlier from Redfish connector
        :param name: Name to search
        :return: List of tuples containing info about found
        value and its parent
        """
        found = []
        for endpoint, data in self.data.items():
            # print(endpoint)  # print searched endpoints
            element_list = self.search_recurse(name, data)
            if element_list:
                prefixed_tuples = utils.prefix_tuples(endpoint, element_list)
                found += prefixed_tuples
        return found

    def find(self, name_list, strict=False, data=None, misses=5):
        """
        Finds a field with a "dictionary path" which includes
        all entries in `name_list` in data stored locally retrieved
        earlier from Redfish connector
        :param name_list: List of names in "dictionary path"
        :return: Single object under last entry in name_list
        """
        if strict:
            in_or_eq = operator.eq
        else:
            in_or_eq = operator.contains

        # starting point - default argument
        if data is None:
            data = self.data

        # all names in list have been found
        if not name_list:
            return data

        # we went too deep or cannot iterate over data
        if (not misses and name_list) or not isinstance(data, dict):
            return None

        to_find = name_list[0]
        found = None
        for key, value in data.items():
            if in_or_eq(key, to_find):
                found = self.find(name_list[1:], strict, value, misses)
            else:
                found = self.find(name_list, strict, value, misses-1)
            if found:
                return found

        return None

    def update_recurse(self, endpoint=None, max_depth=3, data=None):
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
        if not data:
            data = {}
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
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
                    data = self.update_recurse(value, max_depth - 1, data)
                if isinstance(value, dict):
                    endpoints = RedfishTools.endpoint_inception(value)
                    for endp in endpoints:
                        data = self.update_recurse(endp, max_depth - 1, data)
        return data

    def update_data(self):
        """
        Basically `recursive_update()` wrapper to retrieve
        whole data from Redfish connector
        """
        self.data = self.update_recurse(self.endpoint)
        self.last_update = datetime.now()

    @staticmethod
    def endpoint_inception(iterable, max_depth=5, endpoints=None):
        """
        We need to go deeper. Aka extract_endpoints().
        Search for every endpoint reference stored in iterable
        (list, dict) object.
        """
        if not endpoints:
            endpoints = []
        if isinstance(iterable, list):
            for elem in iterable:
                endpoints = RedfishTools.endpoint_inception(elem, max_depth - 1, endpoints)
        if isinstance(iterable, dict):
            for key, value in iterable.items():
                if utils.is_iterable(value):
                    endpoints = RedfishTools.endpoint_inception(
                        value,
                        max_depth - 1,
                        endpoints)
                if key == '@odata.id' and value not in endpoints:
                    endpoints.append(value)
        return endpoints

    def parse_odata(self, odata_iterable):
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
