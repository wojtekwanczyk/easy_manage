import argparse
import easy_manage.utils as utils


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
    print(testfish.systems)


if __name__ == '__main__':
    main()
