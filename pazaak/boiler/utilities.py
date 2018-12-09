from django.http import HttpRequest, HttpResponse


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