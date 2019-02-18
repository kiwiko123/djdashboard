import random
from django.http import HttpRequest, HttpResponse
from .bases import Serializable


class allow_cors:
    def __init__(self, method: callable):
        self._method = method

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self._method(request)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response


def serialize(**payload) -> dict:
    """
    Recursively serializes the keyword arguments into a payload that JsonResponse should be able to consume.
    Any object in the kwargs derived from Serializable will use their `.json()` method.
    Returns the serialized kwargs as a dictionary.
    """
    for field, value in payload.items():
        if isinstance(value, list):
            payload[field] = [serialize(item) for item in value]
        elif isinstance(value, dict):
            payload[field] = serialize(**value)
        elif isinstance(value, Serializable):
            payload[field] = value.json()

    return payload


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
    return random.randrange(1) == 0