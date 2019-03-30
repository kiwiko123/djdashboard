import random


def first_true(iterable, predicate=None, default=None):
    """
    Returns the first item in iterable for which predicate returns True.
    By default, predicate will evaluate the identity (truthy-ness) of each item in iterable.
    If nothing is True, returns default.
    """
    iterator = filter(predicate, iterable)
    return next(iterator, default)


def coin_flip() -> bool:
    """
    Randomly returns True or False.
    """
    return random.randrange(2) == 0


def _is_builtin_field(member: (str, object)) -> bool:
    name, _ = member
    return name.startswith('__') and name.endswith('__')
