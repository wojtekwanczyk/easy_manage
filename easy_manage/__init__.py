import argparse
import pprint as pp
import logging
import json

from pymongo import MongoClient
from easy_manage.controllers.ipmi_controller import IpmiController
from easy_manage.controllers.redfish_controller import RedfishController
from easy_manage.systems.redfish_system import RedfishSystem

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


def main():
    config = parse_conf('config.json')

    LOGGER.info('Welcome to easy_manage!')
    args = parse_args()

    mongo_client = MongoClient(config['database uri'])
    db = mongo_client.get_database(config['database name'])

    rc = RedfishController('controller_test', args.address, db)
    rc.fetch()
    print('== controller ==')
    pp.pprint(rc.data)

    rs = RedfishSystem('system_test', rc, '/redfish/v1/Systems/1')
    rs.fetch()
    print('== system ==')
    pp.pprint(rs.data)

    power = rs.get_power_state()
    print(f"Power state: {power}")

    status = rs.get_status()
    print(f"Status: {status}")

    # LOGGER.info('IPMI TEST')
    # test_ipmi = IpmiController('test_ipmi', args.address)
    # test_ipmi.show_device_id()
    # test_ipmi.show_functions()
    # test_ipmi.show_firmware_version()


if __name__ == '__main__':
    main()
