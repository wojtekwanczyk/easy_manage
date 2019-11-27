"""
RedfishConnector class
"""
import json
import logging
import redfish
from easy_manage.tools import RedfishTools
from easy_manage.exceptions import BadHttpResponse

from .connector import Connector

LOGGER = logging.getLogger('RedfishConnector')
LOGGER.setLevel(logging.DEBUG)


class RedfishConnector(Connector, RedfishTools):
    "Class responisbile for connection through Redfish standard."

    def __init__(self, address, credentials, port=None):
        super().__init__(address, credentials, port)
        self.url = 'https://' + self.address
        self.endpoint = '/redfish/v1'
        self.client = None
        self.connector = self
        self.systems = None

    def connect(self, timeout=7):
        "Connect to Redfish device(s)"

        try:
            self.client = redfish.redfish_client(
                base_url=self.url,
                username=self.credentials.username,
                password=self.credentials.password,
                timeout=timeout,
                max_retry=3)
            self.client.login(auth='session')
            self.connected = True
        except redfish.rest.v1.RetriesExhaustedError as ex:
            LOGGER.error(f"Error while logging in: Too many retires\n{ex}")
            return False
        except json.decoder.JSONDecodeError as ex:
            LOGGER.error(f"Error while logging in: Wrong server response\n{ex}")
            return False
        except redfish.rest.v1.InvalidCredentialsError as ex:
            LOGGER.error(f"Error while logging in: Invalid credentials\n{ex}")
            return False
        return True

    def disconnect(self):
        self.client.logout()

    def test_connection(self):
        if self.connect():
            self.disconnect()
            return True
        return False

    def get_systems(self):
        "Get systems"
        systems = self.get_data(self.endpoint + '/Systems')['Members']
        self.systems = list(self._parse_odata(systems).values())
        return self.systems

    def get_info(self):
        "Get basic connector info"
        return self._get_basic_info()

    def event_subscription(self, destination):
        "Subscribe for events"
        body = {
            'Destination': destination,
            'Context': 'user1_test',
            'EventTypes': ['Alert', 'StatusChange'],
            'Protocol': 'Redfish'}
        res = self.connector.client.post(
            self.endpoint + '/EventService/Subscriptions',
            body=body)
        if res.status >= 300:
            LOGGER.debug(res.text)
            raise BadHttpResponse(res.status)

    # TODO test evenets when webapp api is ready
    def _test_event(self):
        """Triggering Redfish test event.
        Probably not working because of faulty Redfish implementation"""
        endpoint = self.endpoint + "/EventService/Actions/EventService.SubmitTestEvent"
        body = {
            'EventType': 'Alert',
            'EventId': '12345',
            'EventTimestamp': '2017-11-23T17:17:42+00:00',
            'Message': 'Test event',
            'MessageArgs': [
                'EthernetInterface 1',
                '/redfish/v1/Systems/1'],
            'MessageId': '2137',
            'OriginOfCondition': '/redfish/v1/',
            'Severity': 'Warning'}
        return self.client.post(endpoint, body=body)
