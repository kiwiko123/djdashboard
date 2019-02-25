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
    def get(self, request: HttpRequest) -> JsonResponse:
        self.new_game()
        return JsonResponse({})


class EndTurnView(PazaakGameAPI):

    @classmethod
    def url(cls) -> str:
        return '/api/end-turn'

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> JsonResponse:
        payload = json.loads(request.body)

        print('POST - EndTurnView')
        print(payload)

        context = self.process_post(payload)
        print('Context:', context)
        return JsonResponse(context)


class StandView(PazaakGameAPI):

    @classmethod
    def url(cls) -> str:
        return '/api/stand'

    @method_decorator(allow_cors)
    def post(self, request: HttpRequest) -> JsonResponse:
        payload = json.loads(request.body)

        print('POST - StandView')

        context = self.process_post(payload)
        return JsonResponse(context)