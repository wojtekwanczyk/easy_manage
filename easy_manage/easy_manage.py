import redfish
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Placeholder for description')
    parser.add_argument('--socket')
    args = parser.parse_args()

    # FIXME - only for testing
    if not args.socket:
        args.socket = '127.0.0.1:5000'

    return args


def main():
    print('Start')

    args = parse_args()
    print(args.socket)


if __name__ == '__main__':
    main()
