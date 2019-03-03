import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from pazaak.api.game import PazaakGameAPI
from pazaak.helpers.utilities import allow_cors


class NewGameView(PazaakGameAPI):
    @classmethod
    def url(cls) -> str:
        return '/api/new-game'

    @method_decorator(allow_cors)
    def get(self, request: HttpRequest) -> HttpResponse:
        game_id = self.new_game()
        game = self.retrieve_game(game_id)
        context = game.json()
        context['gameId'] = game_id
        return JsonResponse(context)

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        if 'gameId' in payload:
            game_id = payload['gameId']
            self.remove_game(game_id)
        return self.get(request)


class EndTurnView(PazaakGameAPI):
    @classmethod
    def url(cls) -> str:
        return '/api/end-turn'

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class StandView(PazaakGameAPI):
    @classmethod
    def url(cls) -> str:
        return '/api/stand'

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)


class SelectHandCardView(PazaakGameAPI):
    @classmethod
    def url(cls) -> str:
        return '/api/select-hand-card'

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> HttpResponse:
        payload = json.loads(request.body)
        context = self.process_post(payload)
        return JsonResponse(context)