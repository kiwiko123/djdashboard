from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import logging
import re

from .lights.controller import LightController


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# flick#web admin
bridge_ip_address = ''
admin_username = ''

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'flick/index.html'


class LoginView(generic.TemplateView):
    template_name = 'flick/login.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page load """
        assert request.method == 'GET', 'expected GET request; received {0}'.format(request.method)
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page submit """
        assert request.method == 'POST', 'expected POST request; received {0}'.format(request.method)
        return render(request, template_name=self.template_name, context=context)


class CreateAccountView(generic.TemplateView):
    template_name = 'flick/create-account.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page load """
        assert request.method == 'GET', 'expected GET request; received {0}'.format(request.method)
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page submit """
        assert request.method == 'POST', 'expected POST request; received {0}'.format(request.method)
        return render(request, template_name=self.template_name, context=context)


class LightControllerView(generic.TemplateView):
    template_name = 'flick/light-controller.html'
    controller = LightController(bridge_ip_address, admin_username)
    lights = {}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        print('get')
        self._refresh_lights()
        lights = sorted(self.lights.values(), key=lambda d: d['name'])
        context = {'lights': lights}
        return render(request, template_name=self.template_name, context=context)


    def post(self, request: HttpRequest) -> HttpResponse:
        print('post')
        print(request.POST)
        context = self.process_post(request.POST)
        return render(request, template_name=self.template_name, context=context)


    def process_post(self, data: dict) -> dict:
        """
        Processes the HTTP POST data received from the site.
        Returns a context dictionary to be passed back to the site (empty if no data).

        Expected commands:
        -----------------
        TOGGLE
        REFRESH
        """
        context = {}
        if 'command' not in data:
            raise KeyError('failed to receive "command" from AJAX response')
        command = data['command'].upper()
        logger.debug(command)

        if command == 'TOGGLE':
            self._toggle_light(data)
        elif command == 'REFRESH':
            pass

        self._refresh_lights()
        return context


    def _toggle_light(self, data: dict):
        """
        Toggles the given light represented by 'data'.
        If it's on, turns it off, and vice versa.

        'data' is a JSON-serialized dictionary representing one light.
        """
        html_id = data['uniqueid']
        unique_id = self._extract_light_id(html_id)
        light_data = self.lights[unique_id]
        light_number = light_data['number']
        self.controller.toggle(light_number, light_data)



    @staticmethod
    def _extract_light_id(html_id: str) -> str:
        """
        Extracts the unique ID from the given HTML ID.
        'html_id' is expected in the following form:

        "btn-light-{UNIQUE:ID}"

        Example:
        'btn-light-00:11:22:33' -> '00:11:22:33'

        Raises ValueError if html_id is completely unable to match the expected pattern.
        Raises KeyError if the group name is mismatched.
        """
        pattern = 'btn-light-(?P<unique_id>.*)'
        match = re.match(pattern, html_id)
        if match is None:
            raise ValueError('failed to extract unique id from "{0}"'.format(html_id))
        if 'unique_id' not in match.groupdict():
            raise KeyError('group "unique_id" not matched in pattern')
        return match.group('unique_id')


    @classmethod
    def _refresh_lights(cls) -> None:
        """
        Updates cls.lights with refreshed information.
        Stores lights in a dictionary with a single light's uniqueid as each key,
        and serialized JSON dictionary of that light as each value.
        """
        cls.lights = {light['uniqueid']: light for light in cls.controller.lights()}