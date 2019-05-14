"""
Module containing helpers for easy_manage package
"""
from datetime import datetime
from collections import Iterable
import redfish


class BadHealthState(Exception):  # pylint: disable=missing-docstring
    pass


class Controller:
    """
    Base Controller class.
    """
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.socket = ':'.join([address, port])
        self.url = 'http://' + self.socket
        self.last_update = datetime.now()


class RedfishController(Controller):
    """
    Class for data retrieved from controller through
    Redfish standard.
    """
    def __init__(self, name, address, port):
        super(RedfishController, self).__init__(name, address, port)

        self.data = {}
        self.api = '/redfish/v1'
        self.client = redfish.redfish_client(base_url=self.url)
        self.root = self.get_data(self.api)

        root_resources = self.root.get('Links')
        self.root_resources = self.parse_odata(root_resources)

        systems = self.get_data(self.root_resources.get('Systems'))\
            .get('Links')\
            .get('Members')
        self.systems = self.parse_odata(systems)

    @staticmethod
    def parse_odata(odata_iterable):
        """
        Exchange useless @odata keys in a dictionary
        for more readable keys
        """
        if not odata_iterable:
            return None
        parsed_dict = {}
        for key, value in odata_iterable.items():
            parsed_dict[key] = value['@odata.id']
        return parsed_dict

    def get_data(self, endpoint):
        """Get data from endpoint. Wrapper for redfish client"""
        resp = self.client.get(endpoint)
        return resp.dict

    def get_system(self, index):
        """Get system information by index"""
        if not self.systems:
            return None
        return self.get_data(self.systems[index])

    # FIXME: transform to search locally in
    # FIXME: self.data updated by recursive_update
    def recursive_search(self, structure, name, max_depth=3, endpoint=None):
        if max_depth == 0:
            return None
        if isinstance(structure, dict):
            for key, value in structure.items():
                if key == '@odata.id':
                    if value == endpoint:
                        continue
                    resp = self.get_data(value)
                    self.recursive_search(resp, name, max_depth-1, value)
                else:
                    self.recursive_search(value, name, max_depth-1)
                    if endpoint and name in (key, value):
                        print(f'From {endpoint}\n\t{key}: {value}')
        elif isinstance(structure, list):
            for elem in structure:
                self.recursive_search(elem, name, max_depth-1)

    def recursive_update(self, endpoint=None, max_depth=3, data=None):
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
                    data = self.recursive_update(value, max_depth-1, data)
                if isinstance(value, dict):
                    endpoints = RedfishController.endpoint_inception(value)
                    for endp in endpoints:
                        data = self.recursive_update(endp, max_depth-1, data)
        return data

    def update_data(self):
        """
        Basically `recursive_update()` wrapper to retrieve
        whole data from Redfish controller
        """
        self.data = self.recursive_update(self.api)
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
                endpoints = RedfishController.endpoint_inception(elem, max_depth - 1, endpoints)
        if isinstance(iterable, dict):
            for key, value in iterable.items():
                if isinstance(value, Iterable):
                    endpoints = RedfishController.endpoint_inception(value,
                                                                     max_depth - 1,
                                                                     endpoints)
                if key == '@odata.id' and value not in endpoints:
                    endpoints.append(value)
        return endpoints


class IpmiController(Controller):
    """
    Class for data retrieved from controller through
    IPMI standard.
    """
    def __init__(self, name, address, port):
        super(IpmiController, self).__init__(name, address, port)
        raise NotImplemented
