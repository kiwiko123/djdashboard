

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