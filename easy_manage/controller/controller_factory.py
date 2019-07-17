from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.controller.controller import Controller
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.systems.redfish_system import RedfishSystem


# todo: enum for possible interfaces should be created

class ControllerFactory:
    """Class responsible for creating controller,
     it detects available interfaces and adds components corresponding to them with pinch of abstraction"""

    def __init__(self, db):
        self.db = db

    def create_controller(self, name, description, address, credentials):
        controller = Controller(name, description, self.db)
        self.check_standards(controller, address, credentials)
        self.assign_system(controller)
        print(f"SYSTEMS: {controller.systems_interfaces}")
        return controller

    #  TODO: should be static but redfish connector needs db
    def check_standards(self, controller, address, credentials):
        rf_conn = RedfishConnector('test_connector_redfish', address, self.db, credentials)
        if rf_conn.connect():
            controller.standards['redfish'] = rf_conn

        ipmi_conn = IpmiConnector('test_connector_ipmi', address, credentials)
        if ipmi_conn.connect():
            controller.standards['ipmi'] = ipmi_conn
        print(f"STANDARDS: {controller.standards.keys()}")

    def assign_system(self, controller):
        system = controller.system
        for key, connector in controller.standards.items():
            if key == 'redfish':
                # TODO does system endpoint changes?
                system = RedfishSystem('test_system_redfish', connector, '/redfish/v1/Systems/1')
            elif key == 'ipmi':
                system = IpmiSystem('test_system_ipmi', connector)
            # todo: how to implement dir for these or should I abandon it?
            controller.systems_interfaces[key] = system
            new_methods = self.method_difference(system, controller.system)
            self.assign_methods(controller.system, system, new_methods)
        print(dir(controller.system))

    @staticmethod
    def assign_methods(recipient, donor, methods):
        for method in methods:
            setattr(recipient, method, getattr(donor, method))

    @staticmethod
    def method_difference(first, second):
        return set(dir(first)) - set(dir(second))
