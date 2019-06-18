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
    if not args.address:
        args.address = '172.16.67.120'
    args.port = '5000'

    return args


def main():
    print('ok')
    args = parse_args()

    # testfish = RedfishController('testfish', args.address, args.port)
    # test_sys = testfish.systems
    # print(test_sys)
    # testfish.data = testfish.update_recurse('/redfish/v1/Systems/System-1')
    # # print('end')
    # # pprint.pprint(testfish.data)
    # print('Search')
    # found = testfish.find('Health')
    # pprint.pprint(found)

    test_ipmi = IpmiController('test_ipmi', '172.16.67.120', '623')
    test_ipmi.show_device_id()
    test_ipmi.show_functions()
    test_ipmi.show_firmware_version()


if __name__ == '__main__':
    main()
