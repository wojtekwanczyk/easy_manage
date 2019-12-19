import unittest
from unittest import TestCase
from unittest.mock import Mock, PropertyMock, patch

from easy_manage.tools.ipmi.ipmi_backend import IpmiBackend


class IpmiBackendTestCase(TestCase):

    @staticmethod
    def mock_connector():
        "Mocks ipmi connector instance"
        connector = Mock()
        connector.address = PropertyMock(return_value="192.168.1.1")
        mocked_credentials = Mock()
        mocked_credentials.username = PropertyMock(return_value="usrname")
        mocked_credentials.password = PropertyMock(return_value="passwd")
        connector.credentials = Mock(return_value=mocked_credentials)
        connector.ipmi = Mock()
        return connector

    @staticmethod
    def mock_caps_object(intrusion_sensor=0, frontpanel_lockout=0, diagnostic_interrupt=0, power_interlock=0):
        "Mock chassis capabilities object response"
        capabilities = Mock()
        cap_flags = Mock()
        cap_flags.intrusion_sensor = intrusion_sensor
        cap_flags.frontpanel_lockout = frontpanel_lockout
        cap_flags.diagnostic_interrupt = diagnostic_interrupt
        cap_flags.power_interlock = power_interlock
        capabilities.capabilities_flags = cap_flags
        return capabilities

    @staticmethod
    def mock_chassis_status(
            power_on=True, overload=True, interlock=True,
            fault=True, control_fault=True, restore_policy=True,
            last_event=True, chassis_state=True
    ):
        chassis_status = Mock()
        chassis_status.power_on = power_on
        chassis_status.overload = overload
        chassis_status.interlock = interlock
        chassis_status.fault = fault
        chassis_status.control_fault = control_fault
        chassis_status.restore_policy = restore_policy
        chassis_status.last_event = last_event
        chassis_status.chassis_state = chassis_state
        return chassis_status

    def setUp(self):
        self.connector = IpmiBackendTestCase.mock_connector()

    def test_chassis_functions(self):
        self.connector.ipmi.send_message_with_name = Mock(
            return_value=IpmiBackendTestCase.mock_caps_object(
                intrusion_sensor=1,
                diagnostic_interrupt=1
            )
        )
        response = self.connector.ipmi.send_message_with_name()
        ipmi_backend = IpmiBackend(self.connector)
        functions = ipmi_backend.chassis_functions()
        self.assertIn('Physical security sensor', functions)
        self.assertIn('Diagnostic interrupt', functions)
        self.assertNotIn('Power interlock', functions)

    def test_chassis_status(self):
        self.connector.ipmi.get_chassis_status = Mock(
            return_value=IpmiBackendTestCase.mock_chassis_status(
                power_on=False
            )
        )
        ipmi_backend = IpmiBackend(self.connector)
        status = ipmi_backend.chassis_status()
        self.assertEqual(status['chassis_status']['power_on'], False)
