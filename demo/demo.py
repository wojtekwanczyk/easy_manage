"Project base module"

import logging
import json

from easy_manage import (
    IpmiConnector,
    RedfishConnector,
    SshConnector,
    ControllerFactory,
    utils
)
from easy_manage.systems.redfish_system import RedfishSystem
from easy_manage.chassis.redfish_chassis import RedfishChassis
from easy_manage.systems.ipmi_system import IpmiSystem
from easy_manage.chassis.ipmi_chassis import IpmiChassis
from easy_manage.shells.bash_shell import BashShell
from easy_manage.tools.protocol import Protocol

logging.basicConfig(format='%(message)s')
LOGGER = logging.getLogger('easy_manage')
LOGGER.setLevel(logging.DEBUG)


def parse_conf(filename, name='LENOVO'):
    with open(filename) as config_file:
        data = json.load(config_file)
    return data[name]


def redfish_demo(bmc_ip_address, credentials):
    "Just some Redfish testing cases"

    LOGGER.info('Redfish demo')
    rf_conn = RedfishConnector(bmc_ip_address, credentials)
    LOGGER.debug("Connecting to Redfish...")
    if not rf_conn.connect():
        LOGGER.info("Unable to connect to redfish")
        return None, None, None

    LOGGER.debug("Connected")
    rf_sys = RedfishSystem(rf_conn)
    rf_cha = RedfishChassis(rf_conn)

    return rf_sys, rf_cha, rf_conn


def ipmi_demo(bmc_ip_address, credentials):
    LOGGER.info('IPMI demo')
    ipmi_conn = IpmiConnector(bmc_ip_address, credentials)
    ipmi_conn.connect()
    ipmi_sys = IpmiSystem(ipmi_conn)
    #sys = ipmi_sys.aggregate()
    ipmi_chass = IpmiChassis(ipmi_conn)
    #chasis = ipmi_chass.aggregate()
    #sys['events']['discrete_events'] = sys['events']['discrete_events'][0:10]
    print("setting ipmi state: ")
    ipmi_chass.power_up()
    print("IPMI POWER STATE: " + str(ipmi_chass.get_power_state()))
    # return sys,chasis
    # with open('ipmi_out_sys.json', 'w') as f:
    #     json.dump(sys, f, indent=4)
    # #
    # with open('ipmi_out_chassis.json', 'w') as f:
    #     json.dump(chasis, f, indent=4)


#    FRU FETCHING
# frus = ipmi_sys.FRU.component_info()
# SDR FETCHING
# sdrs = ipmi_sys.SDRRepository.fetch_sdr_object_list()

# Fru to sdr matching attempt [*] rip on p
# def wrapper_matching(sdr_id):
#     def matching(x):
#         print(f"Compare {x['fru_id']} with {sdr_id}")
#         return int(x['fru_id']) == int(sdr_id)
#     return matching

# for sdr in sdrs:
# sdr_id = sdr.record_key['sensor_number'] >> 1
# print(f"Trying to match {sdr.record_key}")

# matching = list(filter(wrapper_matching(sdr_id), frus))
# if matching:
# print("Matched some frus with sdrs")
# print(matching)
# print(sdr.name)
# else:
# print("No match\n")

# READING SENESRS
# readings = ipmi_sys.Sensor.mass_read_sensor(sdrs)

# for k, v in readings.items():
# print(f'{{{k}: {v}}}')

# SEL FETCHING
# thresh_evts = ipmi_sys.SEL.threshold_events()
# print(f'Fetched {len(thresh_evts)} threshold events from the system event log')
# for evt in thresh_evts:
# print(evt.data)
# discre_evts = ipmi_sys.SEL.discrete_events()
# for evt in discre_evts:
# print(evt.data)
# print(f'Fetched {len(discre_evts)} threshold events from the system event log')


def shell_demo(system_ip_address, credentials):
    conn = SshConnector(system_ip_address, credentials)
    LOGGER.info("Connecting through ssh")
    res = conn.connect()
    LOGGER.info("Connected:" + str(res))
    if not res:
        return None, None

    sh = BashShell(conn)
    LOGGER.info('Shell obtained')
    # sh.interactive_shell()
    LOGGER.info(sh.readings())
    return sh, conn


def controller_factory_demo(bmc_ip_address, system_ip_address, bmc_credentials, system_credentials):
    configurations = {
        Protocol.REDFISH: {
            'address': bmc_ip_address,
            'credentials': bmc_credentials
        },
        Protocol.IPMI: {
            'address': bmc_ip_address,
            'credentials': bmc_credentials
        },
        Protocol.BASH: {
            'address': system_ip_address,
            'credentials': system_credentials
        },
    }
    controller = ControllerFactory.get_controller(configurations)
    LOGGER.info(ControllerFactory.get_methods(controller.system))
    LOGGER.info(ControllerFactory.get_methods(controller.chassis))
    return controller


def main():
    "Demo program"
    LOGGER.info("Welcome to easy_manage demo!")
    config = parse_conf('config.json', 'LENOVO')

    user_password = input("Provide password: ")

    # example_credentials = Credentials('username', 'password')
    bmc_credentials = utils.get_credentials(config, 'CONTROLLER', user_password)
    system_credentials = utils.get_credentials(config, 'DEVICE', user_password)

    # example_ip_address = '172.16.67.120'
    bmc_ip_address = config['CONTROLLER']['ADDRESS']
    system_ip_address = config['DEVICE']['ADDRESS']

    global rf, c, sh, cont, r_conn, s_conn
    ipmi_demo(bmc_ip_address, bmc_credentials)
    rf, c, r_conn = redfish_demo(bmc_ip_address, bmc_credentials)
    cont = controller_factory_demo(bmc_ip_address, system_ip_address, bmc_credentials, system_credentials)
    sh, s_conn = shell_demo(system_ip_address, system_credentials)

    return 0


if __name__ == '__main__':
    main()
