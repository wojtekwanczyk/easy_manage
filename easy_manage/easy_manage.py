import argparse
import utils
import pprint


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

    testfish = utils.RedfishController('testfish', args.address, args.port)
    test_sys = testfish.systems[0]
    print(test_sys)
    testfish.data = testfish.update_recurse('/redfish/v1/Systems/System-1')
    # print('end')
    # pprint.pprint(testfish.data)
    print('Search')
    found = testfish.find('Health')
    pprint.pprint(found)


if __name__ == '__main__':
    main()
