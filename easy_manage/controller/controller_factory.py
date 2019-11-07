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


class ControllerFactory:
    "Class responsible for creating controllers, it detects available interfaces"
    @staticmethod
    def get_controller(address, credentials, custom_connection=None):
        """
        Create controller detecting with interfaces it can support
        custom_connection is dic of protocols custom settings (port,credentials, address)
        """
        controller = Controller()
        if custom_connection is None:
            custom_connection = {}
        for protocol in Protocols:
            custom = custom_connection.get(protocol, {})
            connection_address = custom.get('address', address)
            connection_credential = custom.get('credentials', credentials)
            connection_port = custom.get('port')
            connector = connectors_switch(
                protocol,
                connection_address,
                connection_credential,
                connection_port)
            if connector and connector.connect():
                controller.standards[protocol] = connector
                system = systems_switch(protocol, connector)
                if system:
                    controller.systems_interfaces[protocol] = system
                    ControllerFactory.assign_missing_methods(controller.system, system)

                chassis = chassis_switch(protocol, connector)
                if chassis:
                    controller.chassis_interfaces[protocol] = chassis
                    ControllerFactory.assign_missing_methods(controller.chassis, chassis)

        LOGGER.info(f"SYSTEMS: {controller.systems_interfaces}")
        LOGGER.info(f"STANDARDS: {controller.standards.keys()}")
        return controller

    @staticmethod
    def get_methods(component):
        "Return all public(not beginning with _) methods from given object"
        return [method_name for method_name in dir(component)
                if callable(getattr(component, method_name)) and not method_name.startswith('_')]

    @staticmethod
    def assign_missing_methods(recipient, donor):
        "Reassigns available methods call from donor to recipient"
        new_methods = list(set(ControllerFactory.get_methods(donor))
                           - set(ControllerFactory.get_methods(recipient)))
        for method in new_methods:
            setattr(recipient, method, getattr(donor, method))
