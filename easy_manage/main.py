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


def parse_conf(filename):
    with open(filename) as config_file:
        data = json.load(config_file)
    return data['LENOVO']

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


def shell_demo(config, credentials):
    sh = BashShell(config['DEVICE']['ADDRESS'], credentials)
    print("Connecting through ssh")
    sh.connect()
    print("Connected")

    cmd = None
    while cmd != 'end':
        cmd = input()
        print(sh.execute(cmd))
    return sh

def main():
    "Main program function"
    LOGGER.info("Welcome to easy_manage!")
    config = parse_conf('config.json')

    mongo_client = MongoClient(config['DATABASE']['NAME'])
    db = mongo_client.get_database(config['DATABASE']['NAME'])
    user_password = 'pass'
    creds_controller = utils.get_credentials(config, 'CONTROLLER', user_password)
    creds_device = utils.get_credentials(config, 'DEVICE', user_password)

    global rf, c, sh
    rf, c = redfish_demo(config, db, creds_controller)
    #ipmi_demo(args, db, creds_controller)
    #sh = shell_demo(config, creds_device)

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
