# This module defines the Pazaak API endpoints with which the client will communicate.
# Django isn't the greatest framework to design an API (maybe unless you're using Django REST),
# so there is some uniqueness in how these views work.
#
# 1. Each view represents an endpoint.
# 2. All views are derived from PazaakGameView, which is derived from View and AutoParseableViewURL.
# 3. Automatic view and URL registration.
#    AutoParseableViewURL allows you to override the @classmethod url() and return the endpoint that this view represents.
#    By doing this, you do not need to explicitly register this view in pazaak/urls.py --
#    they will be automatically picked up and registered on server startup.
# 4. Allowing Cross-Origin Resource Sharing (CORS).
#    Because the server and client are operating on separate ports, we need to enable CORS on the server-side.
#    I've written an @allow_cors(...) decorator that's meant to decorate a View's get() and post() methods.
#    It takes in the client's URL, and a RequestType (GET, POST, or OPTIONS).
# 5. Maintaining game state between Views.
#    In lieu of passing the entire game's data back-and-forth through each request,
#    PazaakGameView stores a static collection of games that each view can access.
#    This is explained more in detail in pazaak/server/game.py,
#    but it does mean that all views _must_ be derived from PazaakGameView.
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse, JsonResponse

from pazaak import data_access, helpers
from pazaak.server.game import PazaakGameView
from pazaak.server.url_tools import AutoParseableViewURL
from pazaak.server.utilities import allow_cors, RequestType
from pazaak.utilities.functions import contains_all_keys


# TODO find a more central place for this function
def client_url() -> str:
    return 'http://localhost:3000'

_CLIENT_URL = client_url()
_ERROR_KEY = 'errorMessage'

class NewGameView(PazaakGameView):
    @staticmethod
    def url() -> str:
        return '/api/new-game'

    @allow_cors(_CLIENT_URL, RequestType.GET)
    def get(self) -> HttpResponse:
        game_count = self.game_manager.game_count()
        print(game_count)
        if game_count and game_count % 10 == 0:
            self.game_manager.clean_games()

        game_id = self.game_manager.new_game()
        game = self.game_manager.get_game(game_id)
        context = game.json()
        context['gameId'] = game_id

        return JsonResponse(context)

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        if 'gameId' in payload:
            game_id = payload['gameId']
            self.game_manager.remove_game(game_id)
        return self.get(request)


class EndTurnView(PazaakGameView):
    @staticmethod
    def url() -> str:
        return '/api/end-turn'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class StandView(PazaakGameView):
    @staticmethod
    def url() -> str:
        return '/api/stand'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class SelectHandCardView(PazaakGameView):
    @staticmethod
    def url() -> str:
        return '/api/select-hand-card'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class CreateAccountView(View, AutoParseableViewURL):
    @staticmethod
    def url() -> str:
        return '/create-account'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        The sole purpose of this override is to remove all CSRF requirements on requests.
        This may not be suitable if Pazaak is ever used in a production environment.
        """
        return super().dispatch(request, *args, **kwargs)

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        context = {}
        payload = json.loads(request.body)
        if contains_all_keys(payload, 'emailAddress', 'password'):
            email_address = payload['emailAddress']
            password = payload['password']
            if email_address and password:
                helpers.accounts.create_user(email_address, password)
                context['emailAddress'] = email_address
            else:
                context[_ERROR_KEY] = 'blank emailAddress or password'
        else:
            context[_ERROR_KEY] = 'missing emailAddress or password from payload'

        return JsonResponse(context)


class LoginView(View, AutoParseableViewURL):
    @staticmethod
    def url() -> str:
        return '/login'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        The sole purpose of this override is to remove all CSRF requirements on requests.
        This may not be suitable if Pazaak is ever used in a production environment.
        """
        return super().dispatch(request, *args, **kwargs)

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        context = {}
        payload = json.loads(request.body)
        if contains_all_keys(payload, 'emailAddress', 'password'):
            email_address = payload['emailAddress']
            password = payload['password']
            if helpers.accounts.are_user_credentials_valid(email_address, password):
                context['emailAddress'] = email_address
            else:
                context[_ERROR_KEY] = 'Invalid credentials. Please try again.'
        else:
            context[_ERROR_KEY] = 'missing emailAddress or password from payload'

        return JsonResponse(context)