import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator

from .game import cards
from .api.game import PazaakGameAPI
from .helpers.utilities import allow_cors, serialize


class NewGameView(PazaakGameAPI):

    @classmethod
    def url(cls) -> str:
        return '/api/new-game'

    @method_decorator(allow_cors)
    def get(self, request: HttpRequest) -> HttpResponse:
        self.new_game()
        move = cards.random_card(positive_only=True, bound=self.game.max_modifier)
        # self.game().end_turn(Turn.PLAYER, move)

        context = serialize(
            player=self.game.player,
            opponent=self.game.opponent,
            move=move,
            status='start'
        )

        return JsonResponse(context)


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
