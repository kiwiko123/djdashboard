from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import json

from .game import cards
from .game.game import PazaakGame

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'pazaak/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return super().get(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        print('post')
        print(request.POST)

        return render(request, template_name=self.template_name, context={})


class PlayView(generic.TemplateView):
    template_name = 'pazaak/play.html'
    _game = PazaakGame(cards.random_cards(4, positive_only=False, bound=5))

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request: HttpRequest) -> HttpResponse:
        print('GET - PlayView')
        context = {'player': self._game.player, 'opponent': self._game.opponent, 'status': 'start'}
        PlayView._game = PazaakGame(cards.random_cards(4, positive_only=False))
        return render(request, self.template_name, context=context)


    def post(self, request: HttpRequest) -> JsonResponse:
        print('POST - PlayView')
        print(request.POST)
        if request.is_ajax():
            context = self._process_post(request.POST)
            print('Context:', context)
            return JsonResponse(context)
        else:
            # shouldn't have gone here in the first place
            return self.get(request)



    def _process_post(self, post_data: dict) -> dict:
        if self._game.game_over():
            return self._process_game_over()

        context = self._process_player_move(post_data)
        content = self._game.json()
        turn = post_data['turn']
        assert turn in content, 'expected turn to be one of ("player", "opponent")'
        context.update(content[turn])
        return context


    def _process_player_move(self, post_data: dict) -> dict:
        if 'action' not in post_data:
            return {}

        action = post_data['action']
        action = action.strip().lower()
        context = {}
        status = ''

        # player end turn
        if action == 'end-turn':
            status = 'play'
            move = cards.random_card(positive_only=True, bound=self._game.max_modifier)
            self._game.make_move(self._game.player, move)
        elif action == 'ready-opponent':
            move = cards.random_card(positive_only=True, bound=self._game.max_modifier)
            self._game.make_move(self._game.opponent, move)
            status = 'end-turn-opponent'
        elif action == 'stand-player':
            self._game.player.stand()
            status = 'stand-player'
        else:
            pass

        context['status'] = status
        return context


    def _process_game_over(self) -> dict:
        winner_code = self._game.winner()
        assert winner_code is not None, 'game is not over'
        switch = {
            self._game.PLAYER_WINS: 'player',
            self._game.OPPONENT_WINS: 'opponent',
            self._game.TIE: 'tie'
        }

        return {
            'status': 'game_over',
            'winner': switch[winner_code]
        }