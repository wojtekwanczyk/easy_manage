"""
Module containing RedfishController class
"""
from datetime import datetime
import redfish
from easy_manage import utils
from .controller import Controller
import pprint as pp


class RedfishController(Controller):
    """
    Class for data retrieved from controller through
    Redfish standard.
    """

    def __init__(self, name, address, port):
        super(RedfishController, self).__init__(name, address, port)

        self.data = {}
        self.api = '/redfish/v1'
        try:
            self.client = redfish.redfish_client(
                base_url=self.url,
                username='student',
                password='VaSIkFFzIyU76csoa8JM')
            self.client.login(auth='session')
        except:
            print("Error while logging in")
        
        self.root = self.get_data(self.api)
        pp.pprint(self.root)

        # root_resources = self.root.get('Links')
        # self.root_resources = self.parse_odata(root_resources)

        redfish_leaf = 'Systems'
        print(f"===== {redfish_leaf} =====")
        endp = self.root.get(redfish_leaf)['@odata.id']
        self.systems = self.get_data(endp) \
            # .get('Links') \
            # .get('Members')
        res = self.get_data('/redfish/v1/Systems')
        pp.pprint(res)

    def get_data(self, endpoint):
        """Get data from endpoint. Wrapper for redfish client"""
        resp = self.client.get(endpoint)
        return resp.dict

    def get_system(self, index):
        """Get system information by index"""
        if not self.systems:
            return None
        return self.get_data(self.systems[index])

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
                elif name in (key, value):
                    tuple_list.append((key, value))
        elif isinstance(structure, list):
            for elem in structure:
                tuple_list += self.search_recurse(name, elem, i + 1)
        return tuple_list

    def find(self, name):
        """
        Find `name` in data stored locally retrieved
        earlier from Redfish controller
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
                    endpoints = RedfishController.endpoint_inception(value)
                    for endp in endpoints:
                        data = self.update_recurse(endp, max_depth - 1, data)
        return data

    def update_data(self):
        """
        Basically `recursive_update()` wrapper to retrieve
        whole data from Redfish controller
        """
        self.data = self.update_recurse(self.api)
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
                if utils.is_iterable(value):
                    endpoints = RedfishController.endpoint_inception(value,
                                                                     max_depth - 1,
                                                                     endpoints)
                if key == '@odata.id' and value not in endpoints:
                    endpoints.append(value)
        return endpoints

    @staticmethod
    def parse_odata(odata_iterable):
        """
        Exchange useless @odata keys in a dictionary
        for more readable keys
        """
        if not odata_iterable:
            return None
        parsed_dict = dict()
        if isinstance(odata_iterable, list):
            for index, elem in enumerate(odata_iterable):
                parsed_dict[index] = elem['@odata.id']
        else:
            for key, value in odata_iterable.items():
                parsed_dict[key] = value['@odata.id']
        return parsed_dict
