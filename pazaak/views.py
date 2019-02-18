import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from pazaak.api.game import PazaakGameAPI
from pazaak.game import cards
from pazaak.helpers.bases import serialize
from pazaak.helpers.utilities import allow_cors


class NewGameView(PazaakGameAPI):

    @classmethod
    def url(cls) -> str:
        return '/api/new-game'

    @method_decorator(allow_cors)
    def get(self, request: HttpRequest) -> HttpResponse:
        self.new_game()
        return HttpResponse()


class EndTurnView(PazaakGameAPI):

    @classmethod
    def url(cls) -> str:
        return '/api/end-turn'

    @method_decorator(allow_cors)
    def post(self, request: HttpResponse) -> JsonResponse:
        payload = json.loads(request.body)

        print('POST - EndTurnView')
        print(payload)

        context = self.process_post(payload)
        print('Context:', context)
        return JsonResponse(context)
