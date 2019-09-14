import abc
import enum
import inspect
import pathlib
import sys

from django.http import HttpResponse

from server.serialization import SerializableEnum


@enum.unique
class RequestType(enum.Enum):
    GET = 'GET'
    POST = 'POST'


class allow_cors:
    def __init__(self, url: str, method_type: RequestType):
        self._url = url
        self._method_type = method_type

    def __call__(self, method: callable):
        signature = inspect.signature(method)
        num_params = len(signature.parameters)

        def _interceptor(*args, **kwargs) -> HttpResponse:
            args = args[:num_params]
            response = method(*args, **kwargs)
            response['Access-Control-Allow-Origin'] = self._url
            response['Access-Control-Allow-Methods'] = self._method_type.value
            response['Access-Control-Max-Age'] = 1000
            response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
            return response

        return _interceptor


def get_client_url() -> str:
    return 'http://localhost:3000'


if __name__ == '__main__':
    pass