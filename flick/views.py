from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import json
import logging
import urllib.error

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
        lights = []

        try:
            lights = self.refresh_lights()
        except urllib.error.URLError as e:
            e.reason = 'check bridge_ip_address and admin_username global variables in views.py'
            logger.error(e.reason)
            raise

        context = {'lights': lights, 'lights_json': json.dumps(lights)}
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
            self.toggle_light(data)
            light_number = self._verify_light_number(data['number'])
            context['toggled_light_number'] = json.dumps(light_number)
        elif command == 'REFRESH':
            pass

        lights = self.refresh_lights()
        context['lights'] = lights
        context['lights_json'] = json.dumps(lights)

        return context


    def toggle_light(self, data: dict):
        """
        Toggles the given light represented by 'data'.
        If it's on, turns it off, and vice versa.

        'data' is a JSON-serialized dictionary representing one light,
        received from the AJAX request triggered when toggling a light on/off.
        """
        light_number = self._verify_light_number(data['number'])
        light_data = self.lights[light_number]
        self.controller.toggle(light_number, light_data)


    @staticmethod
    def _verify_light_number(number_from_data: str) -> str:
        """
        Verifies that number_from_data is an integer.
        Returns the number as an `int` object.

        number_from_data is the value associated with the key 'number' from the AJAX response when toggling a light,
        e.g., data['number'].

        Example:
        '1' -> 1

        Raises ValueError if number_from_data is not a string representation of an integer.
        """
        number_from_data = number_from_data.strip()
        if not number_from_data.isdigit():
            raise ValueError(
                'expected to receive an integer unique light number; instead received "{0}"'.format(number_from_data))
        return int(number_from_data)


    @classmethod
    def refresh_lights(cls) -> [dict]:
        """
        Updates cls.lights with refreshed information.
        Stores lights in a dictionary with a single light's uniqueid as each key,
        and serialized JSON dictionary of that light as each value.
        """
        cls.lights = {light['number']: light for light in cls.controller.lights()}
        lights = []
        for light in cls.lights.values():
            info = {k: light[k] for k in ('name', 'number')}
            info['on'] = light['state']['on']
            lights.append(info)

        return sorted(lights, key=lambda d: d['name'])