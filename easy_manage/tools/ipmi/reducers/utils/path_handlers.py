from easy_manage.tools.ipmi.reducers.constants.exceptions import InvalidPathError, CorruptedBufferError


def bare_validate_paths(dictionary, *args):
    "Method which returns boolean value according to all given paths being valid"
    for path in args:
        work_dict = {**dictionary}  # Restore dict
        for prop in path:
            try:
                work_dict = work_dict[prop]
            except KeyError:
                raise InvalidPathError(path)


def validate_paths(dictionary, *args):
    "Method dedicated to buffer validating"
    try:
        bare_validate_paths(dictionary, *args)
    except InvalidPathError as ip_err:
        raise CorruptedBufferError(f'Buffer doesn\'t have path: {ip_err.path}')


def extract_by_path(dictionary, path_lst):
    work_dict = dict(dictionary)
    for elem in path_lst:
        work_dict = work_dict[elem]
    return work_dict
