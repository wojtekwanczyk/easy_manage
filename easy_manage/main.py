"Project base module"

import argparse
import pprint as pp
import logging
import json

from pymongo import MongoClient
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.chassis.redfish_chassis import RedfishChassis
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.controller.controller_factory import ControllerFactory
from easy_manage.utils import utils
from easy_manage.shells.bash_shell import BashShell


logging.basicConfig(format='%(message)s')
LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)


def parse_conf(filename, name='LENOVO'):
    with open(filename) as config_file:
        data = json.load(config_file)
    return data[name]

def redfish_demo(config, db, credentials):
    "Just some Redfish testing cases"

    LOGGER.info('Redfish demo')

    global rf_conn
    rf_conn = RedfishConnector('test_connector_redfish', config['CONTROLLER']['ADDRESS'], db, credentials)
    LOGGER.debug("Connecting to Redfish...")
    rf_conn.connect() # without this data is taken from db
    LOGGER.debug("Connected")

    rf_sys = RedfishSystem('test_system_redfish',
                           rf_conn, '/redfish/v1/Systems/1')
    rf_cha = RedfishChassis('test_chassis_redfish', rf_conn, '/redfish/v1/Chassis/1')

    # power = rf_sys.get_power_state()
    # print(f"Power state: {power}")
    # rf_sys.power_on()
    # status = rf_sys.get_system_health()
    # print(f"Status: {status}")

    # cmd = None
    # while cmd != 'end':
    #     cmd = input()
    #     d = rf_sys.get_data("/redfish/v1/" + cmd)
    #     pp.pprint(d)

    return rf_sys, rf_cha


def ipmi_demo(args, db, credentials):
    LOGGER.info('IPMI demo')
    ipmi_conn = IpmiConnector('test_connector_ipmi',
                              args.address, db, credentials)
    print(ipmi_conn.connect())
    # ipmi_conn.show_device_id()
    # ipmi_conn.show_functions()
    # ipmi_conn.show_firmware_version()
    #print('========= ' + ipmi_conn.ipmi.connected)
    ipmi_sys = IpmiSystem('test_system_ipmi', ipmi_conn)
    power = ipmi_sys.get_power_state()
    print(f"Power state: {power}")


def redfish_save(rf, ch):

    def system(rf):

        res = {}

        r = {}
        r['basic info'] = rf.get_info()
        r['oem info'] = rf.get_oem_info()
        r['power state'] = rf.get_power_state()
        r['system health'] = rf.get_system_health()
        r['memory size'] = rf.get_memory_size()

        r['allowable boot sources'] = rf.get_allowable_boot_sources()
        r['boot source'] = rf.get_boot_source()

        coolers = rf.get_coolers()
        fans = coolers['/redfish/v1/Chassis/1/Thermal']['Fans'][0]
        r['coolers'] = fans

        r['chassis'] = rf.get_chassis()
        r['power supplies'] = rf.get_power_supplies()
        r['managers'] = rf.get_managers()

        r['cpu summary'] = rf.get_processor_summary()
        r['cpu info'] = rf.get_processor_info(1)
        r['cpu data'] = rf.get_processor_data(1)
        hist = rf.get_cpu_history_performance()
        hist['Container'] = hist['Container'][:4]
        r['cpu history performance'] = hist
        hist = rf.get_cpu_history_power()
        r['cpu history power'] = hist['Container'][0:3]

        r['ethernet interfaces'] = rf.get_ethernet_interfaces()
        r['storage'] = rf.get_storage()
        r['memory'] = rf.get_memory()
        r['pcie devices'] = rf.get_pcie_devices()
        r['pcie functions'] = rf.get_pcie_functions()
        logs = rf.get_standard_logs()
        logs["Members"] = logs['Members'][0]
        r['standard logs'] = logs
        #r['active logs'] = rf.get_active_logs()

        res['system'] = r

        with open('out_system.json', 'w') as f:
            json.dump(res, f)

    def chassis(ch):

        c = {}

        c['basic info'] = ch.get_info()
        c['oem info'] = ch.get_oem_info()
        c['power state'] = ch.get_power_state()
        c['health'] = ch.get_health()


        c['thermal health'] = ch.get_thermal_health()
        c['example temp'] = ch.get_temperature('Ambient Temp')
        c['example fan spd'] = ch.get_fan_speed('Fan 1 Tach')
        c['power info'] = ch.get_power_info()
        c['power control'] = ch.get_power_control()
        c['power supply example'] = ch.get_power_supply(0)
        c['power voltages example'] = ch.get_power_voltage(0)
        c['power redundancy'] = ch.get_power_redundancy()
 
        c['network adapters'] = ch.get_network_adapters()
        c['storage'] = ch.get_storage()
        c['pcie devices'] = ch.get_pcie_devices()
        c['drives'] = ch.get_drives()
        c['managers'] = ch.get_managers()

        with open('out_chassis.json', 'w') as f:
            json.dump(c, f)
    
    chassis(ch)


def shell_demo(config, credentials):
    sh = BashShell(config['DEVICE']['ADDRESS'], credentials)
    print("Connecting through ssh")
    sh.connect()
    print("Connected")
    #sh.interactive_shell()    
    return sh

def main():
    "Main program function"
    LOGGER.info("Welcome to easy_manage!")
    config = parse_conf('config.json', 'LENOVO')

    mongo_client = MongoClient(config['DATABASE']['NAME'])
    db = mongo_client.get_database(config['DATABASE']['NAME'])
    user_password = 'pass'
    creds_controller = utils.get_credentials(config, 'CONTROLLER', user_password)
    creds_device = utils.get_credentials(config, 'DEVICE', user_password)

    global rf, c, sh
    rf, c = redfish_demo(config, db, creds_controller)
    redfish_save(rf, c)
    #ipmi_demo(args, db, creds_controller)
    # sh = shell_demo(config, creds_device)

    # controller_factory = ControllerFactory()
    # controller = controller_factory.create_controller(
    #     'name',
    #     'description',
    #     args.address,
    #     credentials,
    #     db)
    # print(f"POWER STATE: {controller.get_power_state()}")
    return 0


if __name__ == '__main__':
    main()
