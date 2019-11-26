"""
Module with class responsible for correct creation of controllers that can be used
without knowledge of which interfaces they use
"""
import logging

from easy_manage.controller.controller import Controller
from easy_manage.connectors.connectors_switch import connectors_switch
from easy_manage.tools.protocol import ProtocolNotHandled

from . import COMPONENTS

LOGGER = logging.getLogger('ControllerFactory')
LOGGER.setLevel(logging.INFO)


class ControllerFactory:
    "Class responsible for creating controllers, it detects available interfaces"

    @staticmethod
    def _get_connectors(config, address=None, credentials=None):
        "Create controllers relying on passed config"
        connectors = {}
        for interface, configuration in config.items():
            connection_address = configuration.get('address', address)
            connection_credential = configuration.get('credentials', credentials)
            connection_port = configuration.get('port')
            try:
                connector = connectors_switch(
                    interface,
                    connection_address,
                    connection_credential,
                    connection_port)
            except ProtocolNotHandled:
                LOGGER.info(f"CAN'T CREATE CONNECTOR FOR: {interface}")
                continue
            connector.connect()
            connectors[interface.value] = connector
        return connectors
    
    @staticmethod
    def _inject_interfaces(controller, connectors):
        "Injects interfaces from connectors to controller components"
        for component, interfaces in COMPONENTS.items():
            for interface, interface_class in interfaces.items():
                interface_instance = interface_class(connectors[interface])

                component_dict = controller.components.get(component, {})
                component_dict[interface] = interface_instance
                controller.components[component] = component_dict

                ControllerFactory.assign_missing_methods(
                    controller[component],
                    interface_instance)

    @staticmethod
    def get_controller(config, address=None, credentials=None):
        """
        Create controller detecting with interfaces it can support
        :param config: dictinary with schema {protocol: {address, credentials, port}}
        :param address: default address if not passed in config
        :param credentials: default credentials if not passed in config
        :return: Created controller
        """
        controller = Controller()
        connectors = ControllerFactory._get_connectors(
            config, address, credentials)
        ControllerFactory._inject_interfaces(controller, connectors)

        LOGGER.info(f"COMPONENTS: {controller.components}")
        LOGGER.info(f"INTERFACES: {controller.standards.keys()}")
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
