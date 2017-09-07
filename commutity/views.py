import logging
import django.core.exceptions
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views import generic
from . import helper, models
from .authentication import info
from .authentication.encryption import PasswordEncryptor


logger = logging.getLogger(__name__)
ERROR_CTX = 'error'


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
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        context = {}
        if self._verify_user(username, password):
            # valid - login, redirect home
            logger.info('login user "{0}"'.format(username))
            request.session['user'] = helper.get_user(username)
            request.session['info'] = info.LoginInfo(username)
            context['username'] = username
            return render(request, template_name=IndexView.template_name, context=context)
        else:
            context.clear()
            context[ERROR_CTX] = 'invalid username "{0}"'.format(username)
        return render(request, template_name=self.template_name, context=context)
        

    @staticmethod
    def _verify_user(username: str, password: str) -> bool:
        credentials = helper.get_credentials(username)
        manager = PasswordEncryptor(key=credentials.key, iv=credentials.iv)
        return manager.encrypt(password) == credentials.password


class LogoutView(generic.TemplateView):
    template_name = IndexView.template_name

    def get(self, request: HttpRequest) -> HttpResponse:
        print('get logout')
        if 'user' in request.session:
            user = request.session['user']
            info = request.session['info']
            info.log_out()
            print(helper.default_obj_str(info, 'username', 'time_in', 'time_out'))
            del request.session['user']
        else:
            # raise Http404('user not recorded in session')
            return redirect('commutity:index')
        return super().get(request)