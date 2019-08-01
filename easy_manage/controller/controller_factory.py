"""
Module with class responsible for correct creation of controllers that can be used
without knowledge of which interfaces they use
"""

from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.controller.controller import Controller
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.systems.redfish_system import RedfishSystem


# todo: enum for possible interfaces should be created

class ControllerFactory:
    "Class responsible for creating controllers, it detects available interfaces"

    def __init__(self, db):
        self.db = db

    def create_controller(self, name, description, address, credentials):
        "Create controller detecting with interfaces it can support"
        controller = Controller(name, description, self.db)
        self.discover_standards(controller, address, credentials)
        self.assign_system(controller)
        print(f"SYSTEMS: {controller.systems_interfaces}")
        return controller

    #  TODO: should be static but redfish connector needs db
    def discover_standards(self, controller, address, credentials):
        "Detects which standards can be used on given server"
        rf_conn = RedfishConnector('test_connector_redfish', address, self.db, credentials)
        if rf_conn.connect():
            controller.standards['redfish'] = rf_conn

        ipmi_conn = IpmiConnector('test_connector_ipmi', address, credentials)
        if ipmi_conn.connect():
            controller.standards['ipmi'] = ipmi_conn
        print(f"STANDARDS: {controller.standards.keys()}")

    def assign_system(self, controller):
        system = controller.system
        for name, connector in controller.standards.items():
            if name == 'redfish':
                # TODO does system endpoint changes?
                system = RedfishSystem('test_system_redfish', connector, '/redfish/v1/Systems/1')
            elif name == 'ipmi':
                system = IpmiSystem('test_system_ipmi', connector)
            controller.systems_interfaces[name] = system
            self.assign_missing_methods(controller.system, system)

    @staticmethod
    def assign_missing_methods(recipient, donor):
        "Reassigns available methods call from donor to recipient"
        if recipient.abstract:
            new_methods = donor.get_methods()
            recipient.abstract = False
        else:
            new_methods = list(set(donor.methods) - set(recipient.methods))
        for method in new_methods:
            setattr(recipient, method, getattr(donor, method))
