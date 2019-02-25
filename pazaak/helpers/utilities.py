import random
from django.http import HttpRequest, HttpResponse


class allow_cors:
    def __init__(self, method: callable):
        self._method = method
        self._whitelisted_urls = 'http://localhost:3000'    # TODO (1) specify in decoration, (2) accept multiple

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self._method(request)
        response['Access-Control-Allow-Origin'] = self._whitelisted_urls
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response


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