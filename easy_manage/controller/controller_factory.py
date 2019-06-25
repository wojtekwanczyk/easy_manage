from easy_manage.controller.controller import Controller
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.systems.ipmi_system import IpmiSystem

class ControllerFactory:

    def create_controller(self, name, description, address, username, password, db):
        controller = Controller(name, description)

        rf_conn = RedfishConnector('test_connector_redfish', address, db)
        if rf_conn.connect():
            controller.standards.append('redfish')
            rf_sys = RedfishSystem('test_system_redfish', rf_conn, '/redfish/v1/Systems/1')
            controller.systems.append(rf_sys)
        
        ipmi_conn = IpmiConnector('test_connector_ipmi', address, db)
        if ipmi_conn.connect():
            controller.standards.append('ipmi')
            ipmi_sys = IpmiSystem('test_system_ipmi', ipmi_conn)
            controller.systems.append(ipmi_sys)
        
        print(f"SYSTEMS: {controller.systems}")
        
        return controller
