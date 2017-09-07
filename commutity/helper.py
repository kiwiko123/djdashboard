import os.path
import pathlib
import re
import django.core.exceptions
import commutity
from commutity.models import Credentials, User


def get_app_directory() -> pathlib.Path:
    """ Returns a Path object pointing to the app's base directory """
    result = os.path.dirname(commutity.__file__)
    return pathlib.Path(result)


def get_properties_file() -> pathlib.Path:
    """ Returns a Path object pointing to commutity/properties.xml """
    app_dir = get_app_directory()
    return pathlib.Path('{0}/properties.xml'.format(app_dir.as_posix()))


def get_user(username: str) -> User or None:
	""" Returns the User object matching 'username',
		or None if no matching user is found.
	"""
	try:
		return User.objects.get(username=username)
	except django.core.exceptions.MultipleObjectsReturned:
		assert False, 'username is not unique; model design flawed'
	except django.core.exceptions.ObjectDoesNotExist:
		return None

def get_credentials(username: str) -> Credentials:
	""" Returns the Credentials object associated with 'username'.
		Raises ValueError (or traced AssertionError) if invalid.
	"""
	user = get_user(username)
	if user is None:
		raise ValueError('username "{0}" does not exist'.format(username))

	try:
		return Credentials.objects.get(user=user)
	except django.core.exceptions.ObjectDoesNotExist:
		assert False, 'username is not unique; model design flawed'

def generic_obj_str(obj: object, *instance_vars, invasive=False) -> str:
    """ Provides a generic __str__ implementation for any object.
        If invasive=True, processes obj.__dict__ for @property attributes to display.
        Otherwise, iterates through *instance_vars for EXACT instance variable name matches.
        Raises AttributeError on an incorrect name.

        Generates a string in the form of 'Class(attr1=value1, attr2=value2, ...)'
    """
    attributes = ''
    if invasive:
        for name, value in obj.__dict__.items():
            if not re.match('^__[^_]+__$') and isinstance(value, property):
                value = eval('{0}.{1}'.format('obj', v))
                attributes += '{0}={1}, '.format(v, value)
    else:
        for v in instance_vars:
            value = eval('{0}.{1}'.format('obj', v))
            attributes += '{0}={1}, '.format(v, value)
    return '{0}({1})'.format(type(obj).__name__, attributes[:-2])