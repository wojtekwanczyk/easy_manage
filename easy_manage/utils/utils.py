"""
Module containing helpers for easy_manage package
"""

import hashlib
import base64
from collections import namedtuple
from cryptography.fernet import Fernet
from easy_manage.exceptions import InvalidCredentials
from easy_manage.tools import ProtocolNotHandled


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


def get_credentials(config, name, user_password):
    """Get decrypted credentials relying on user password.
    `name` is parsed from config file"""
    hashed_password = config['USER_PASSWORD']
    if hashlib.sha256(user_password.encode()).hexdigest() != hashed_password:
        raise InvalidCredentials

    password_encrypted = config[name]['PASSWORD']
    user_password_with_padding = user_password + '=' * (32 - len(user_password))
    key = base64.urlsafe_b64encode(user_password_with_padding.encode())
    fernet = Fernet(key)
    password = fernet.decrypt(password_encrypted.encode()).decode()

    credentials = Credentials(
        config[name]['USERNAME'],
        password)

    return credentials


def encrypt(user_password, password):
    user_password_with_padding = user_password + '=' * (32 - len(user_password))
    key = base64.urlsafe_b64encode(user_password_with_padding.encode())
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()


def raise_protocol_error():
    raise ProtocolNotHandled
