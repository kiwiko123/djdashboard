from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import logging

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
    lights = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        print('get')
        self._refresh_lights()
        context = {'lights': lights}
        return render(request, template_name=self.template_name, context=context)


    def post(self, request: HttpRequest) -> HttpResponse:
        print('post')
        print(request.POST)
        context = {}
        return render(request, template_name=self.template_name, context=context)


    @classmethod
    def _refresh_lights(cls) -> None:
        cls.lights = cls.controller.lights()
        cls.lights.sort(key=lambda d: d['name'])