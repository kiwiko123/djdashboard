import inspect
import logging
import math
import os
import pathlib
import re
import uuid
from flick.security import encryption

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

__reference_dir = 'properties'
__reference_file = 'credentials.txt'

_iv_label = 'iv'
_bridge_ip_label = 'bridge_ip_address'
_api_username_label = 'api_username'


def _get_current_directory() -> pathlib.Path:
    """
    Returns a Path object to the directory of the currently-executing module.
    """
    frame = inspect.currentframe()
    this_module = inspect.getfile(frame)
    path = pathlib.Path(this_module)
    return path.parent


def make_key() -> str:
    """
    Returns a normalized (length-16) string representation of the computer's MAC address.
    """
    mac_address = str(uuid.getnode())
    size = len(mac_address)
    needed = encryption.PasswordEncryptor.required_length
    multiplier = math.ceil((needed - size) / needed) + 1
    result = mac_address * multiplier
    return result[:needed]


def get_encrypted_values(bridge_ip_address: str, api_username: str) -> (bytes,):
    """
    Returns a 3-tuple of (initialization vector, bridge_ip_address, api_username).
    Initialization vector is randomly generated.
    """
    mac_address = make_key()
    encryptor = encryption.PasswordEncryptor(key=mac_address)
    encrypted_ip = encryptor.encrypt(bridge_ip_address)
    encrypted_username = encryptor.encrypt(api_username)

    return encryptor.iv, encrypted_ip, encrypted_username


def read_encrypted_values(infile: open) -> (bytes,):
    """
    Parses infile for credential properties.
    Returns a 3-tuple of found credentials:

    (initialization vector, encrypted bridge IP address, encrypted API username)
    """
    pattern = '(?P<key>[^=]+)=(?P<value>.+)'
    compiled = re.compile(pattern)
    properties = {}

    for line in infile:
        line = line.strip()
        match = compiled.match(line)
        if match is None:
            raise KeyError('failed to parse credentials file')
        key, value = match.group('key'), match.group('value')
        value = eval(value)
        if type(value) is not bytes:
            raise TypeError("expected encrypted credentials to resemble a 'bytes' object")
        properties[key] = value

    return properties[_iv_label], properties[_bridge_ip_label], properties[_api_username_label]


def export_encrypted_values(outfile: open, iv: bytes, encrypted_bridge_ip_address: bytes, encrypted_api_username: bytes) -> None:
    """
    Writes the encrypted values to 'outfile', in the format:

    iv=b'xxxxxxx'
    bridge_ip_address=b'xxxxxxx'
    api_username=b'xxxxxx'
    """
    if not all(type(e) is bytes for e in (encrypted_bridge_ip_address, encrypted_api_username)):
        raise TypeError("expected encrypted arguments to be type 'bytes'")
    outfile.write('iv={0}\n'.format(iv))
    outfile.write('bridge_ip_address={0}\n'.format(encrypted_bridge_ip_address))
    outfile.write('api_username={0}'.format(encrypted_api_username))


def authenticate() -> (str, str):
    """
    Attempts to authenticate the user by determining the
      * IP address of the Philips Hue bridge, and
      * username of the account accessing the API.

    Expects a file named 'credentials.txt' to reside under the relatively-local directory './properties' -
    or more specifically, under flick/security/properties.
    'credentials.txt' is expected to store the decryptor's initialization vector, and encrypted credentials described above.

    If this file does not exist, it will prompt the user (currently via console) to enter in both values.
    'credentials.txt' will be created, encrypting the values before being written to the file.
    A random initialization vector is generated.

    Credentials are 256-bit AES-encrypted using a normalized string of your computer's MAC address as the key.
    Thus, credentials will have to be re-created between different computers.

    Returns a 2-tuple of the decrypted/plaintext (bridge IP address, API username).
    """
    iv = None
    bridge_ip = None
    api_username = None
    key = make_key()
    encryptor = encryption.PasswordEncryptor(key=key)
    current_directory = _get_current_directory()
    credentials_location = '{0}/{1}/{2}'.format(current_directory, __reference_dir, __reference_file)
    credentials_path = pathlib.Path(credentials_location)

    if credentials_path.is_file():
        with credentials_path.open() as infile:
            # attempt to read 'credentials.txt', and decrypt its values.
            try:
                iv, e_bridge_ip, e_api_username = read_encrypted_values(infile)
                encryptor.iv = iv
                bridge_ip = encryptor.decrypt(e_bridge_ip)
                api_username = encryptor.decrypt(e_api_username)

            # if an exception is thrown while reading the existing 'credentials.txt', OR
            # while decrypting the read-values,
            # delete the existing 'credentials.txt' and have the user make a new one.
            except (KeyError, TypeError, encryption.DecryptionError) as e:
                logger.error("exception of type {0} - failed to read and/or decrypt 'credentials.txt'; user must manually re-input credentials".format(type(e)))
                os.remove(credentials_location)
                bridge_ip, api_username = authenticate()

    else:
        iv = encryptor.iv
        bridge_ip = input('Enter the IP address of the Philips Hue bridge: ')
        api_username = input('Enter the username of the API account: ')

        e_bridge_ip = encryptor.encrypt(bridge_ip)
        e_api_username = encryptor.encrypt(api_username)

        with credentials_path.open('w+') as outfile:
            export_encrypted_values(outfile, iv, e_bridge_ip, e_api_username)

    return bridge_ip, api_username