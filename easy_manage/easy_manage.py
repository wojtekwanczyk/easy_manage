import argparse
import easy_manage.utils as utils
import pprint
import utils
from ipmi_controller import IPMIController
from redfish_controller import RedfishController

def parse_args():
    parser = argparse.ArgumentParser(description='Placeholder for description')
    parser.add_argument('--address')
    parser.add_argument('--port')
    args = parser.parse_args()

    # FIXME - only for testing
    args.address = 'localhost'
    args.port = '5000'

    return args


def main():
    args = parse_args()

    testfish = redfish_controller.RedfishController('testfish', args.address, args.port)
    test_sys = testfish.systems[0]
    print(test_sys)
    testfish.data = testfish.update_recurse('/redfish/v1/Systems/System-1')
    # print('end')
    # pprint.pprint(testfish.data)
    print('Search')
    found = testfish.find('Health')
    pprint.pprint(found)


   test_ipmi = IPMIController('test_ipmi', '127.0.0.1', '9001')
    test_ipmi.show_device_id()
    test_ipmi.show_functions()
    test_ipmi.show_firmware_version()
    # print(testfish.systems)

if __name__ == '__main__':
    main()
