from easy_manage.tools.ipmi.reducers.constants.exceptions import InvalidPathError
from easy_manage.tools.ipmi.reducers.utils.path_handlers import bare_validate_paths, extract_by_path


def extract_flat_props(dictionary, path, props):
    "Extracts the props in the list from the dictionary, which are at given path"
    info = {}
    for prop in props:
        try:
            working_path = path.copy()
            working_path.append(prop)
            bare_validate_paths(dictionary, working_path)
            info[prop] = extract_by_path(dictionary, working_path).strip()  # Noticed some unstripped values in JSON
        except InvalidPathError:  # Going to be a none-value
            pass
    return info


def filter_dict_values(validator, dictionary):
    "Filters VALUES of a dictionary, by a given validator "
    ret_val = []
    for _, v in dictionary.items():
        if validator(v):
            ret_val.append(v)
    return ret_val
