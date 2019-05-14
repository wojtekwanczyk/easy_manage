import redfish
from controller import Controller


class RedfishController(Controller):
    def __init__(self, name, address, port):
        super(RedfishController, self).__init__(name, address, port)

        self.client = redfish.redfish_client(base_url=self.url)
        self.root = self.get_endpoint('/redfish/v1')

        root_resources = self.root.get('Links')
        self.root_resources = self.parse_odata(root_resources)

        systems = self.get_endpoint(self.root_resources.get('Systems'))\
            .get('Links')\
            .get('Members')
        self.systems = self.parse_odata(systems)

    @staticmethod
    def parse_odata(odata_iterable):
        if not odata_iterable:
            return None

        parsed_dict = {}
        if isinstance(odata_iterable, list):
            for index, elem in enumerate(odata_iterable):
                parsed_dict[index] = elem['@odata.id']
        else:
            for key, value in odata_iterable.items():
                parsed_dict[key] = value['@odata.id']
        return parsed_dict

    def get_endpoint(self, endpoint):
        resp = self.client.get(endpoint)
        return resp.dict

    @staticmethod
    def safe_get(key, dictionary):
        return dictionary.get(key, '')
