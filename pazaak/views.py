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

from django.http import HttpRequest, HttpResponse, JsonResponse

from pazaak.server.game import PazaakGameView
from pazaak.server.url_tools import client_url
from pazaak.server.utilities import allow_cors, RequestType


_CLIENT_URL = client_url()

class NewGameView(PazaakGameView):
    @classmethod
    def url(cls) -> str:
        return '/api/new-game'

    @allow_cors(_CLIENT_URL, RequestType.GET)
    def get(self) -> HttpResponse:
        game_id = self.new_game()
        game = self.retrieve_game(game_id)
        context = game.json()
        context['gameId'] = game_id
        return JsonResponse(context)

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        if 'gameId' in payload:
            game_id = payload['gameId']
            self.remove_game(game_id)
        return self.get(request)


class EndTurnView(PazaakGameView):
    @classmethod
    def url(cls) -> str:
        return '/api/end-turn'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class StandView(PazaakGameView):
    @classmethod
    def url(cls) -> str:
        return '/api/stand'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class SelectHandCardView(PazaakGameView):
    @classmethod
    def url(cls) -> str:
        return '/api/select-hand-card'

    @allow_cors(_CLIENT_URL, RequestType.POST)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)