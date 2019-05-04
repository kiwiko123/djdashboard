import datetime
import json
import inspect

from django.http import HttpRequest, HttpResponse
from django.views.generic.base import View

from pazaak import data_access, helpers
from pazaak.enums import RequestType
from pazaak.data_access.transfer_objects import UserDTO


ERROR_KEY = 'errorMessage'
CURRENT_USER_KEY = 'currentUser'
EMAIL_ADDRESS_KEY = 'emailAddress'


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


class request_to_payload:
    """
    Method decorator to extract the payload as a dictionary from a Django HttpRequest.
    If the key 'emailAddress' is included in the payload, automatically include a UserDTO representation of the user.
    A typical Django request method looks like:
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        # ...
        return HttpResponse()

    This can be condensed to:
    @request_to_payload
    def post(self, payload: dict) -> HttpResponse:
        # ...
        return HttpResponse()
    """
    def __init__(self, method: callable):
        self._method = method

    def __call__(self, instance: View, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        payload = request.body
        if type(payload) in (bytes, str):
            payload = json.loads(request.body)

        payload = self._payload_with_current_user(payload)
        return self._method(instance, payload, *args, **kwargs)

    def _payload_with_current_user(self, payload: dict) -> dict:
        if CURRENT_USER_KEY in payload:
            raise KeyError('current user key already exists in payload: {0}'.format(payload))

        if EMAIL_ADDRESS_KEY in payload:
            email_address = payload[EMAIL_ADDRESS_KEY]
            if helpers.accounts.is_user_logged_in(email_address):
                user = data_access.users.get_by_email(email_address, raise_exception_on_fail=True)
                payload[CURRENT_USER_KEY] = UserDTO(user)

        return payload



class monitor:
    def __init__(self, function: callable):
        self._function = function
        self._start_time = None
        self._finish_time = None
        self._exception = None

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time

    @property
    def finish_time(self) -> datetime.datetime:
        return self._finish_time

    @property
    def exception(self) -> Exception:
        return self._exception

    def duration(self) -> datetime.timedelta:
        result = None
        if self.start_time and self.finish_time:
            result = self.finish_time - self.start_time
        return result

    def __call__(self, *args, **kwargs):
        result = None

        try:
            self._start_time = datetime.datetime.utcnow()
            result = self._function(*args, **kwargs)
            self._finish_time = datetime.datetime.utcnow()
        except Exception as e:
            self._exception = e
            raise
        finally:
            self._log_metrics()

        return result

    def _log_metrics(self) -> None:
        pass



if __name__ == '__main__':
    pass
