from easy_manage.chassis.constants import PowerState
from easy_manage.tools.ipmi.reducers.constants.exceptions import CorruptedBufferError
from easy_manage.tools.ipmi.reducers.constants.paths import (
    PWR_STATE_PATH, EXHAUST_TEMP_PATH, AMBIENT_TEMP_PATH,
    SYSTEM_POWER_PATH, COMPONENTS_PATH,
)
from easy_manage.tools.ipmi.reducers.filtering_functions import is_pwr, is_fan
from easy_manage.tools.ipmi.reducers.parsing_functions import parse_pwr, parse_fan_spd, extract_components
from easy_manage.tools.ipmi.reducers.utils.misc import filter_dict_values
from easy_manage.tools.ipmi.reducers.utils.path_handlers import validate_paths, extract_by_path


class ChassisReducer:
    class ReadingsReducer:

        @staticmethod
        def power_state(_sys, chass):
            pwr_state = None
            try:
                validate_paths(chass, PWR_STATE_PATH)
                pwr_state = extract_by_path(chass, PWR_STATE_PATH)
                return {
                    True: PowerState.ON,
                    False: PowerState.OFF
                }[pwr_state].value
            except KeyError:
                raise CorruptedBufferError(f'Buffer specified unsupported pwr_state: {pwr_state}')

        @staticmethod
        def exhaust_temp(sys, _chass):
            validate_paths(sys, EXHAUST_TEMP_PATH)
            return extract_by_path(sys, EXHAUST_TEMP_PATH)

        @staticmethod
        def ambient_temp(sys, _chass):
            validate_paths(sys, AMBIENT_TEMP_PATH)
            return extract_by_path(sys, AMBIENT_TEMP_PATH)

        @staticmethod
        def fan_speeds(sys, _chass):
            all_sensors = sys['sensors']
            fans = filter_dict_values(is_fan, all_sensors)
            ret_dict = {}
            for fan in fans:
                ret_dict = {**ret_dict, **parse_fan_spd(fan)}
            return ret_dict

        @staticmethod
        def pwr_consumed(sys, _chass):
            validate_paths(sys, SYSTEM_POWER_PATH)
            return extract_by_path(sys, SYSTEM_POWER_PATH)

    class StaticsReducer:

        @staticmethod
        def pwr_supplies(sys, _chass):
            components = extract_by_path(sys, COMPONENTS_PATH)
            return extract_components(components, is_pwr, parse_pwr)
