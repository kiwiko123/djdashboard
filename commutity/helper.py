import os.path
import pathlib
import commutity


def get_app_directory() -> pathlib.Path:
    """ Returns a Path object pointing to the app's base directory """
    result = os.path.dirname(commutity.__file__)
    return pathlib.Path(result)


def get_properties_file() -> pathlib.Path:
    """ Returns a Path object pointing to commutity/properties.xml """
    app_dir = get_app_directory()
    return pathlib.Path('{0}/properties.xml'.format(app_dir.as_posix()))
