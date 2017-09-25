import logging
import django.core.exceptions
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views import generic
from . import helper, models
from .authentication import info
from .authentication.encryption import PasswordEncryptor


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

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
            request.session['user'] = helper.get_user(username)
            request.session['info'] = info.LoginInfo(username)
            logger.info('{0}'.format(request.session['info']))
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
    template_name = 'commutity/logout.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        print('get logout')
        if 'user' in request.session:
            user = request.session['user']
            info = request.session['info']
            info.log_out()
            logger.info('{0}'.format(info))
            del request.session['user']
        else:
#             raise Http404('user not recorded in session')
            return redirect('commutity:index')
        return render(request, template_name=self.template_name)
    
    
class CreateAccountView(generic.TemplateView):
    template_name = 'commutity/create-account.html'
    
    def get(self, request: HttpRequest) -> HttpResponse:
        return super().get(request)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        print(request.POST)
        received = set(request.POST)
        print(received)
        expected = ('first_name',
                    'last_name',
                    'email',
                    'phone',
                    'username',
                    'password')
        if not all(field in received for field in expected):
            raise Http404('invalid fields')
        
        user = self._make_user(request.POST)
        credentials = self._make_credentials(user, request.POST['password'])
    
        user.save()
        credentials.save()
        
        return render(request, template_name=self.template_name)
    
    @staticmethod
    def _make_user(response: {str: str}) -> models.User:
        username = response['username']
        first_name = response['first_name']
        last_name = response['last_name']
        email = response['email']
        phone = response['phone']
        return models.User(username=username, first_name=first_name, last_name=last_name, phone=phone)
    
    @staticmethod
    def _make_credentials(user: models.User, password: str) -> models.Credentials:
        manager = PasswordEncryptor()
        encrypted = manager.encrypt(password)
        return models.Credentials(user=user, password=encrypted, key=manager.key, iv=manager.iv)