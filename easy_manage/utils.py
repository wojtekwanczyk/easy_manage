import json
import requests


class Controller:
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.socket = ':'.join([address, port])
        self.url = 'http://' + self.socket


class RedfishController(Controller):
    def __init__(self, name, address, port):
        super(RedfishController, self).__init__(name, address, port)

        self.root = self.get_endpoint('/redfish/v1')

        links_odata = self.root.get('Links', '')
        self.links = self.parse_odata(links_odata)

    @staticmethod
    def parse_odata(odata_dict):
        if not odata_dict:
            return odata_dict

        parsed_dict = {}
        for key, value in odata_dict.items():
            parsed_dict[key] = value['@odata.id']
        return parsed_dict

    def get_endpoint(self, endpoint):
        resp = requests.get(self.url + endpoint)
        return resp.json()
