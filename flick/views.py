from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views import generic

import logging


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# flick#web admin
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