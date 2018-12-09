import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .game import cards
from .api.game import PazaakGameAPI
from .boiler.bases import serialize
from .boiler.utilities import allow_cors


class NewGameView(generic.TemplateView, PazaakGameAPI):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(allow_cors)
    def options(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse()

    @method_decorator(allow_cors)
    def get(self, request: HttpRequest) -> JsonResponse:
        self.new_game()
        move = cards.random_card(positive_only=True, bound=self.game().max_modifier)
        # self.game().end_turn(Turn.PLAYER, move)

        context = serialize(
            player=self.game().player,
            opponent=self.game().opponent,
            move=move.modifier,
            status='start'
        )

        return JsonResponse(context)


class EndTurnView(generic.TemplateView, PazaakGameAPI):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(allow_cors)
    def options(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse()

    @method_decorator(allow_cors)
    def post(self, request: HttpResponse) -> JsonResponse:
        payload = json.loads(request.body)

        print('POST - EndTurnView')
        print(payload)

        context = self._process_post(payload)
        print('Context:', context)
        return JsonResponse(context)