import argparse
import pprint as pp
import logging

from easy_manage.controllers.ipmi_controller import IpmiController
from easy_manage.controllers.redfish_controller import RedfishController

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
        LOGGER.debug(f'Default server addres {args.address} has been set')

    return args


def main():

    LOGGER.info('Welcome to easy_manage!')
    args = parse_args()

    testfish = RedfishController('testfish', args.address)
    LOGGER.info('Systems')
    pp.pprint(testfish.systems)
    testfish.data = testfish.update_recurse(list(testfish.systems.keys())[0])
    LOGGER.info('=== Data ===')
    pp.pprint(testfish.data)
    LOGGER.info('=== Search ===')
    found = testfish.find('Name')
    pp.pprint(found)

    LOGGER.info('IPMI TEST')
    test_ipmi = IpmiController('test_ipmi', args.address)
    test_ipmi.show_device_id()
    test_ipmi.show_functions()
    test_ipmi.show_firmware_version()


if __name__ == '__main__':
    main()
