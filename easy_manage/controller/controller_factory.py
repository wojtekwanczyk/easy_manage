"""
Module with class responsible for correct creation of controllers that can be used
without knowledge of which interfaces they use
"""
import logging

from easy_manage.controller.controller import Controller
from easy_manage.protocols import Protocols
from easy_manage.connectors.connectors_switch import connectors_switch
from easy_manage.chassis.chassis_switch import chassis_switch
from easy_manage.systems.system_switch import systems_switch

LOGGER = logging.getLogger('ControllerFactory')
LOGGER.setLevel(logging.INFO)


class ControllerFactory(Controller):
    "Class responsible for creating controllers, it detects available interfaces"

    def __init__(self, name, address, credentials, custom_connection={}):
        """
        Create controller detecting with interfaces it can support
        custom_connection is map of protocols custom settings (port,credentials, address)
        """
        super().__init__(name)
        if custom_connection is None:
            custom_connection = {}
        for protocol in Protocols:
            custom = custom_connection.get(protocol, False)()
            connection_address = address
            connection_credential = credentials
            connection_port = None
            if custom:
                if custom.address:
                    connection_address = custom.address
                if custom.credentials:
                    connection_credential = custom.credentials
                if custom.port:
                    connection_port = custom.port
            connector = connectors_switch(
                protocol,
                connection_address,
                connection_credential,
                connection_port)
            if connector and connector.connect():
                self.standards[protocol] = connector
                system = systems_switch(protocol, connector)
                if system:
                    self.systems_interfaces[protocol] = system
                    ControllerFactory.assign_missing_methods(self.system, system)

                chassis = chassis_switch(protocol, connector)
                if chassis:
                    self.chassis_interfaces[protocol] = chassis
                    ControllerFactory.assign_missing_methods(self.chassis, chassis)

        LOGGER.info(f"SYSTEMS: {self.systems_interfaces}")
        LOGGER.info(f"STANDARDS: {self.standards.keys()}")

    @staticmethod
    def get_methods(component):
        "Returns list of possible methods"
        return [method_name for method_name in dir(component)
                if callable(getattr(component, method_name))
                and not method_name.startswith('_')
                and method_name != 'assign_missing_methods']

    @staticmethod
    def assign_missing_methods(recipient, donor):
        "Reassigns available methods call from donor to recipient"
        new_methods = list(set(ControllerFactory.get_methods(donor))
                           - set(ControllerFactory.get_methods(recipient)))
        for method in new_methods:
            setattr(recipient, method, getattr(donor, method))
