"Project base module"

import argparse
import pprint as pp
import logging
import json
import hashlib
import base64
from cryptography.fernet import Fernet


from pymongo import MongoClient
from easy_manage.connectors.ipmi_connector import IpmiConnector
from easy_manage.connectors.redfish_connector import RedfishConnector
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.chassis.redfish_chassis import RedfishChassis
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.chassis.ipmi_chassis import IpmiChassis
from easy_manage.utils.general_tools import Credentials


logging.basicConfig(format='%(message)s')
LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)


<< << << < Updated upstream
== == == =
<< << << < Updated upstream


def parse_conf(filename, name='LENOVO'):


== == == =
>>>>>> > Stashed changes


def parse_args():
    "Method for parsing arguments from command line"
    parser = argparse.ArgumentParser(description='Placeholder for description')
    parser.add_argument('--address')
    parser.add_argument('--port')
    args = parser.parse_args()

    # FIXME - only for testing
    if not args.address:
        args.address = '172.16.67.120'


<< << << < Updated upstream
   LOGGER.debug(f"Default server address {args.address} has been set")
== == == =
   LOGGER.debug(f'Default server address {args.address} has been set')
>>>>>> > Stashed changes

   return args


def parse_conf(filename):


<< << << < Updated upstream
== == == =
>>>>>> > Stashed changes
>>>>>> > Stashed changes
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

    global rf_conn
    rf_conn = RedfishConnector(
        'test_connector_redfish', args.address, db, credentials)
    rf_conn.connect()  # without this data is taken from db
    rf_conn.fetch()

    rf_sys = RedfishSystem('test_system_redfish',
                           rf_conn, '/redfish/v1/Systems/1')
    rf_sys.fetch()
    rf_cha = RedfishChassis('test_chassis_redfish',
                            rf_conn, '/redfish/v1/Chassis/1')
    rf_cha.fetch()

    power = rf_sys.get_power_state()
    print(f"Power state: {power}")
    rf_sys.power_on()

    status = rf_sys.get_system_health()
    print(f"Status: {status}")

    print(rf_sys.get_memory_size())

    cmd = None
    while cmd != 'end':
        cmd = input()
        d = rf_sys.get_data("/redfish/v1/" + cmd)
        pp.pprint(d)

    return rf_sys, rf_cha


def ipmi_demo(args, db, credentials):
    LOGGER.info('IPMI demo')
    ipmi_conn = IpmiConnector('test_connector_ipmi',
                              args.address, credentials)
    print(ipmi_conn.connect())
    ipmi_sys = IpmiSystem('test_system_ipmi', ipmi_conn)
    ipmi_chass = IpmiChassis(ipmi_conn)
    sdrs = ipmi_sys.SDRRepository.fetch_sdr_object_list()

    for sdr in sdrs:
        print(sdr.name)

    ipmi_chass = IpmiChassis(ipmi_conn)

    # FRU FETCHING
    for fru in ipmi_sys.FRU.component_info():
        print(fru['fru_id'])

    # SDR FETCHING
    # sdrs = ipmi_sys.SDRRepository.fetch_sdr_object_list()
    # readings = ipmi_sys.Sensor.mass_read_sensor(sdrs)
    # for k, v in readings.items():
    #     print(f'{{{k}: {v}}}')

    # SEL FETCHING
    # thresh_evts = ipmi_sys.SEL.threshold_events()
    # print(f'Fetched {len(thresh_evts)} threshold events from the system event log')
    # for evt in thresh_evts:
    # print(evt.data)
    # discre_evts = ipmi_sys.SEL.discrete_events()
    # for evt in discre_evts:
    # print(evt.data)
    # print(f'Fetched {len(discre_evts)} threshold events from the system event log')


def main():
    "Main program function"
    config = parse_conf('config.json')

    LOGGER.info("Welcome to easy_manage!")
    args = parse_args()

    mongo_client = MongoClient(config['database uri'])
    db = mongo_client.get_database(config['database name'])
    credentials = get_credentials(config, 'pass')

    global rf, c
    # rf, c = redfish_demo(args, db, credentials)

    ipmi_demo(args, db, credentials)

    # controller_factory = ControllerFactory()
    # controller = controller_factory.create_controller(
    #     'name',
    #     'description',
    #     args.address,
    #     credentials,
    #     db)
    # print(f"POWER STATE: {controller.get_power_state()}")
    return 0


if __name__ == '__main__':
    main()
