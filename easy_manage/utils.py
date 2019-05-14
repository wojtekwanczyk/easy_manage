"""
Module containing helpers for easy_manage package
"""
from datetime import datetime


class BadHealthState(Exception):  # pylint: disable=missing-docstring
    pass


class Controller:  # pylint: disable=too-few-public-methods
    """
    Base Controller class.
    """
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.socket = ':'.join([address, port])
        self.url = 'http://' + self.socket
        self.last_update = datetime.now()


class IpmiController(Controller):
    """
    Class for data retrieved from controller through
    IPMI standard.
    """
    def __init__(self, name, address, port):
        super(IpmiController, self).__init__(name, address, port)
        raise NotImplemented


def prefix_tuples(string, tuples):
    """
    Appends given string to beginning of first element of every tuple
    :param string: String to append to first element of every tuple
    :param tuples: List of tuples to format
    :return: Formatted list of tuples
    """
    return [('.'.join([string, tup[0]]),) + tup[1:] for tup in tuples]


def is_iterable(structure):
    """Check if given structure is either dictionary or list"""
    return type(structure) in (dict, list)  # pylint: disable=unidiomatic-typecheck
