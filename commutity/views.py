from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'commutity/index.html'


class LoginView(generic.TemplateView):
    template_name = 'commutity/login.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page load """
        assert request.method == 'GET', 'expected GET request; received {0}'.format(request.method)
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        """ Invoked on page submit """
        assert request.method == 'POST', 'expected POST request; received {0}'.format(request.method)
        return render(request, self.template_name, {})
