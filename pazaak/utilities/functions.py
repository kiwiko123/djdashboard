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


def is_from_type(obj: object, type_cls: type) -> bool:
    obj_type = type(obj)
    return isinstance(obj, type_cls) or issubclass(obj_type, type_cls)


def contains_all_keys(table: dict, *keys: str) -> bool:
    return all(key in table for key in keys)