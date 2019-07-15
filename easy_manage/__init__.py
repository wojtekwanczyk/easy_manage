"Project base module"

import argparse
import pprint as pp
import logging
import json
import hashlib
import base64
from cryptography.fernet import Fernet
import imp # just for testing

from pymongo import MongoClient
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.controller.controller_factory import ControllerFactory
from easy_manage.utils import Credentials

#imp.reload(ipmi_connector)

logging.basicConfig(format='%(message)s')
LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)

def parse_args():
    "Method for patsing arguments from command line"
    parser = argparse.ArgumentParser(description='Placeholder for description')
    parser.add_argument('--address')
    parser.add_argument('--port')
    args = parser.parse_args()

    # FIXME - only for testing
    if not args.address:
        args.address = '172.16.67.120'
        LOGGER.debug(f"Default server address {args.address} has been set")

    return args

def parse_conf(filename):
    with open(filename) as config_file:
        data = json.load(config_file)
    return data

def get_credentials(config, user_password):
    hashed_password = config['hashed_password']
    if hashlib.sha256(user_password.encode()).hexdigest() != hashed_password:
        LOGGER.critical("Invalid credetials")
        return 1

    password_encrypted = config['encrypted system password']
    user_password_with_padding = user_password + '='*(32-len(user_password))
    key = base64.urlsafe_b64encode(user_password_with_padding.encode())
    fernet = Fernet(key)
    password = fernet.decrypt(password_encrypted.encode()).decode()

    credentials = Credentials(
        config['username'],
        password)

    return credentials

def redfish_demo(args, db, credentials):
    "Just some Redfish testing cases"

    LOGGER.info('Redfish demo')
    rf_conn = RedfishConnector('test_connector_redfish', args.address, db, credentials)
    # rf_conn.connect() # without this data is taken from db
    rf_conn.fetch()

    rf_sys = RedfishSystem('test_system_redfish', rf_conn, '/redfish/v1/Systems/1')
    rf_sys.fetch()

    power = rf_sys.get_power_state()
    print(f"Power state: {power}")

    status = rf_sys.get_system_health()
    print(f"Status: {status}")

    print(rf_sys.find(["Processor", "State"]))


def ipmi_demo(args, db, credentials):
    LOGGER.info('IPMI demo')
    ipmi_conn = IpmiConnector('test_connector_ipmi', args.address, db, credentials)
    print(ipmi_conn.connect())
    # ipmi_conn.show_device_id()
    # ipmi_conn.show_functions()
    # ipmi_conn.show_firmware_version()
    #print('========= ' + ipmi_conn.ipmi.connected)
    ipmi_sys = IpmiSystem('test_system_ipmi', ipmi_conn)
    power = ipmi_sys.get_power_state()
    print(f"Power state: {power}")

def main():
    "Main program function"
    config = parse_conf('config.json')

    LOGGER.info("Welcome to easy_manage!")
    args = parse_args()

    mongo_client = MongoClient(config['database uri'])
    db = mongo_client.get_database(config['database name'])
    credentials = get_credentials(config, 'pass')

    redfish_demo(args, db, credentials)
    #ipmi_demo(args, db, credentials)

    # controller_factory = ControllerFactory()
    # controller = controller_factory.create_controller(
    #     'name',
    #     'description',
    #     args.address,
    #     credentials,
    #     db)
    # print(f"POWER STATE: {controller.get_power_state()}")


if __name__ == '__main__':
    main()
