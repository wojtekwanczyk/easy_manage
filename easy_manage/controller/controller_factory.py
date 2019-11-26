"""
Module with class responsible for correct creation of controllers that can be used
without knowledge of which interfaces they use
"""
import logging

from easy_manage.controller.controller import Controller
from easy_manage.connectors.connectors_switch import connectors_switch
from easy_manage.chassis.chassis_switch import chassis_switch
from easy_manage.systems.system_switch import systems_switch
from easy_manage.tools.protocol import ProtocolNotHandled

LOGGER = logging.getLogger('ControllerFactory')
LOGGER.setLevel(logging.INFO)


class ControllerFactory:
    "Class responsible for creating controllers, it detects available interfaces"

    @staticmethod
    def get_controller(config, address=None, credentials=None):
        """
        Create controller detecting with interfaces it can support
        :param config: dic of protocol,{address, credentials, port}- values for which controller will be created,
        :param address: default address if not passed in config
        :param credentials: default credentials if not passed in config
        :return: Created controller
        """
        controller = Controller()
        for protocol, configuration in config.items():
            connection_address = configuration.get('address', address)
            connection_credential = configuration.get('credentials', credentials)
            connection_port = configuration.get('port')
            try:
                connector = connectors_switch(
                    protocol,
                    connection_address,
                    connection_credential,
                    connection_port)
                connector.connect()
                controller.standards[protocol] = connector
                try:
                    system = systems_switch(protocol, connector)
                    controller.systems_interfaces[protocol] = system
                    ControllerFactory.assign_missing_methods(controller.system, system)
                except ProtocolNotHandled:
                    LOGGER.info(f"CAN'T CREATE SYSTEM FOR: {protocol}")
                try:
                    chassis = chassis_switch(protocol, connector)
                    controller.chassis_interfaces[protocol] = chassis
                    ControllerFactory.assign_missing_methods(controller.chassis, chassis)
                except ProtocolNotHandled:
                    LOGGER.info(f"CAN'T CREATE CHASSIS FOR: {protocol}")
            except ProtocolNotHandled:
                LOGGER.info(f"CAN'T CREATE CONNECTOR FOR: {protocol}")

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
