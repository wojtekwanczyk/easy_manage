import argparse
import pprint as pp
import logging
import json
import imp # just for testing

from pymongo import MongoClient
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.controller.controller_factory import ControllerFactory

#imp.reload(ipmi_connector)

logging.basicConfig(format='%(message)s')
LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)

def parse_args():
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

def redfish_demo(args, db):
    LOGGER.info('Redfish demo')
    rf_conn = RedfishConnector('test_connector_redfish', args.address, db)
    print(rf_conn.connect()) # without this data is taken from db
    rf_conn.fetch()

    # print('== connector ==')
    # pp.pprint(rf_conn.data)

    rf_sys = RedfishSystem('test_system_redfish', rf_conn, '/redfish/v1/Systems/1')
    rf_sys.fetch()
    # print('== system ==')
    # pp.pprint(rf_sys.data)

    power = rf_sys.get_power_state()
    print(f"Power state: {power}")

    # status = rs.get_status()
    # print(f"Status: {status}")

def ipmi_demo(args, db):
    LOGGER.info('IPMI demo')
    ipmi_conn = IpmiConnector('test_connector_ipmi', args.address, db)
    print(ipmi_conn.connect())
    # ipmi_conn.show_device_id()
    # ipmi_conn.show_functions()
    # ipmi_conn.show_firmware_version()
    #print('========= ' + ipmi_conn.ipmi.connected)
    ipmi_sys = IpmiSystem('test_system_ipmi', ipmi_conn)
    power = ipmi_sys.get_power_state()
    print(f"Power state: {power}")

def main():
    config = parse_conf('config.json')

    LOGGER.info("Welcome to easy_manage!")
    args = parse_args()

    mongo_client = MongoClient(config['database uri'])
    db = mongo_client.get_database(config['database name'])

    #redfish_demo(args, db)
    #ipmi_demo(args, db)

    controller_factory = ControllerFactory()
    controller = controller_factory.create_controller(
        'name',
        'description',
        args.address,
        'student',
        'password',
        db)
    print(f"POWER STATE: {controller.get_power_state()}")

if __name__ == '__main__':
    main()
