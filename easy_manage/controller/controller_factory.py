"""
Module with class responsible for correct creation of controllers that can be used
without knowledge of which interfaces they use
"""
# todo: chasis need to be added to factory
import logging

from easy_manage.controller.controller import Controller
from easy_manage.protocols import Protocols
from easy_manage.systems.system_switch import systems_switch
from easy_manage.connectors.connectors_switch import connectors_switch

LOGGER = logging.getLogger('ControllerFactory')
LOGGER.setLevel(logging.INFO)


class ControllerFactory:
    "Class responsible for creating controllers, it detects available interfaces"

    def create_controller(self, name, description, address, credentials):
        "Create controller detecting with interfaces it can support"
        controller = Controller(name, description)
        for protocol in Protocols:
            connector = connectors_switch(protocol, address, credentials)
            if connector and connector.connect():
                controller.standards[protocol] = connector
                system = systems_switch(protocol, connector)
                if system:
                    controller.systems_interfaces[protocol] = system
                    controller.system.assign_missing_methods(system)

        LOGGER.info(f"SYSTEMS: {controller.systems_interfaces}")
        LOGGER.info(f"STANDARDS: {controller.standards.keys()}")
        return controller
