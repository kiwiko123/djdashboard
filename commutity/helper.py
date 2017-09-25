import os.path
import pathlib
import re
import django.core.exceptions
import commutity
from commutity.models import Credentials, User
from commutity.utilities import exceptions


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
		raise exceptions.AuthenticationError('username "{0}" does not exist'.format(username))

	try:
		return Credentials.objects.get(user=user)
	except django.core.exceptions.ObjectDoesNotExist:
		assert False, 'username is not unique; model design flawed'