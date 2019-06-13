import argparse
import pprint


from easy_manage.controllers.ipmi_controller import IpmiController
from easy_manage.controllers.redfish_controller import RedfishController


def parse_args():
    parser = argparse.ArgumentParser(description='Placeholder for description')
    parser.add_argument('--address')
    parser.add_argument('--port')
    args = parser.parse_args()

    # FIXME - only for testing
    args.address = '172.16.67.120'
    args.port = '5000'

    return args


def main():
    args = parse_args()
    tunnel = {'address': 'jagular.iisg.agh.edu.pl', 'username': 'penis', 'password': 'penis'}

    testfish = RedfishController('testfish', args.address, '443', tunnel)
    test_sys = testfish.systems[0]
    print(test_sys)
    testfish.data = testfish.update_recurse('/redfish/v1/Systems/System-1')
    # print('end')
    # pprint.pprint(testfish.data)
    print('Search')
    found = testfish.find('Health')
    pprint.pprint(found)

    test_ipmi = IpmiController('test_ipmi', args.address, '80', tunnel)
    test_ipmi.show_device_id()
    test_ipmi.show_functions()
    test_ipmi.show_firmware_version()


if __name__ == '__main__':
    main()
