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
        self.new_game()
        context = self.game.json()
        return JsonResponse(context)


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