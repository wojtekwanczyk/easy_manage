from functools import reduce

import easy_manage.tools.ipmi.reducers.constants as constants
from easy_manage.tools.ipmi.reducers.constants.exceptions import InvalidPathError
from easy_manage.tools.ipmi.reducers.constants.paths import (
    POH_PATHS, CPU_UTILIZATION_PATH, CPU_PWR_PATH,
    BOARD_INFO_PATH, PRODUCT_INFO_PATH, HARDWARE_COMPONENTS_PATH,
)
from easy_manage.tools.ipmi.reducers.filtering_functions import is_memory, is_cpu, is_pci
from easy_manage.tools.ipmi.reducers.parsing_functions import (
    parse_memsize, parse_cpu, parse_pci, parse_memory,
    extract_components,
)
from easy_manage.tools.ipmi.reducers.utils.misc import extract_flat_props
from easy_manage.tools.ipmi.reducers.utils.path_handlers import validate_paths, extract_by_path, bare_validate_paths


class SystemReducer:
    class ReadingsReducer:

        @staticmethod
        def poh_counter(_sys, chass):
            validate_paths(chass, *POH_PATHS)
            poh = chass['power_on_counter']
            return poh['minutes_per_count'] * poh['counter_reading']

        @staticmethod
        def cpu_summary_usage(sys, _chass):
            validate_paths(sys, CPU_UTILIZATION_PATH)
            return extract_by_path(sys, CPU_UTILIZATION_PATH)

        @staticmethod
        def cpu_summary_power(sys, _chass):
            validate_paths(sys, CPU_PWR_PATH)
            return extract_by_path(sys, CPU_PWR_PATH)

        @staticmethod
        def cpus_temperatures(sys, _chass):
            cpu_temps = {}
            for cpu_nr in range(constants.MAX_PROCESSORS):
                cpu_temp_path = ['sensors', f'cpu{cpu_nr}_temp', 'reading', 'value']
                try:
                    bare_validate_paths(sys, cpu_temp_path)
                    cpu_temps[f'cpu_{cpu_nr}'] = {}
                    cpu_temps[f'cpu_{cpu_nr}']['temp'] = extract_by_path(sys, cpu_temp_path)
                except InvalidPathError:  # Going to mean just lack of value
                    pass
            return cpu_temps

    class StaticsReducer:
        @staticmethod
        def basic_info(sys, _chass):
            "Motherboard info - board + product info"
            board_info_keys = ['manufacturer', 'product_name', 'serial_number', 'part_number']
            prod_info_keys = ['manufacturer', 'name', 'part_number', 'version', 'serial_number']

            inf1 = extract_flat_props(sys, BOARD_INFO_PATH, board_info_keys)
            inf2 = extract_flat_props(sys, PRODUCT_INFO_PATH, prod_info_keys)
            return {**inf1, **inf2}

        @staticmethod
        def mem_size_gb(sys, _chass):
            components = extract_by_path(sys, HARDWARE_COMPONENTS_PATH)
            rollup = reduce(lambda a, b: a + b, map(parse_memsize, filter(is_memory, components)))
            return rollup

        @staticmethod
        def cpus_info(sys, _chass):
            components = extract_by_path(sys, HARDWARE_COMPONENTS_PATH)
            return extract_components(components, is_cpu, parse_cpu)

        @staticmethod
        def storage_info(sys, _chass):
            components = extract_by_path(sys, HARDWARE_COMPONENTS_PATH)
            storages = extract_components(components, is_memory, parse_memory)
            return [{'name': k, **v} for k, v in storages.items()]  # Fix for schema

        @staticmethod
        def pci_info(sys, _chass):
            components = extract_by_path(sys, HARDWARE_COMPONENTS_PATH)
            return extract_components(components, is_pci, parse_pci)
