from logging import getLogger

from easy_manage.tools.ipmi.reducers.chassis_reducer import ChassisReducer
from easy_manage.tools.ipmi.reducers.system_reducer import SystemReducer

log = getLogger(__name__)


# TODO: Return readings with units or we just assume them? 

class IpmiReducer:
    "Class which reduces ipmi's json-data to data-model"

    def __init__(self, sys_buff, chass_buff):
        self.sys_buffer = sys_buff
        self.chass_buffer = chass_buff

    def reduce_chassis_reading(self):
        return {
            'pwr_state': ChassisReducer.ReadingsReducer.power_state(self.sys_buffer, self.chass_buffer),

            'temperature': {
                'exhaust_temp': ChassisReducer.ReadingsReducer.exhaust_temp(self.sys_buffer, self.chass_buffer),
                'ambient_temp': ChassisReducer.ReadingsReducer.ambient_temp(self.sys_buffer, self.chass_buffer)
            },
            'fans': ChassisReducer.ReadingsReducer.fan_speeds(self.sys_buffer, self.chass_buffer),
            'power_consumed_watts': ChassisReducer.ReadingsReducer.pwr_consumed(self.sys_buffer, self.chass_buffer),

        }

    def reduce_chassis_static(self):
        return {
            'power_supplies': ChassisReducer.StaticsReducer.pwr_supplies(self.sys_buffer, self.chass_buffer)
        }

    def reduce_system_reading(self):
        return {
            'power_on_hours': SystemReducer.ReadingsReducer.poh_counter(self.sys_buffer, self.chass_buffer),
            'cpu_summary': {
                'usage': SystemReducer.ReadingsReducer.cpu_summary_usage(self.sys_buffer, self.chass_buffer),
                'power': SystemReducer.ReadingsReducer.cpu_summary_power(self.sys_buffer, self.chass_buffer),
            },
            # This is just temperatures now, could merge dicts if necessary
            'cpus': SystemReducer.ReadingsReducer.cpus_temperatures(self.sys_buffer, self.chass_buffer),
            # 'events': #TODO: Implement
        }

    def reduce_system_static(self):
        return {
            'basic_info': SystemReducer.StaticsReducer.basic_info(self.sys_buffer, self.chass_buffer),
            'total_memory_size_gb': SystemReducer.StaticsReducer.mem_size_gb(self.sys_buffer, self.chass_buffer),
            'cpus': SystemReducer.StaticsReducer.cpus_info(self.sys_buffer, self.chass_buffer),
            'storage': SystemReducer.StaticsReducer.storage_info(self.sys_buffer, self.chass_buffer),
            'pci_e': SystemReducer.StaticsReducer.pci_info(self.sys_buffer, self.chass_buffer),
            # 'sensors': SystemReducer.StaticsReducer.sensors_info(self.sys_buffer, self.chass_buffer) #TODO: Implement

        }