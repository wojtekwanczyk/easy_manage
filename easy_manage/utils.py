"""
Module containing helpers for easy_manage package
"""

from collections import namedtuple


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
    return isinstance(structure, (list, dict))

Credentials = namedtuple(
    'Credentials', [
        'username',
        'password'])
