from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import re

from .game import cards
from .game.game import PazaakGame, Turn


def _init_game() -> PazaakGame:
    return PazaakGame(cards.random_cards(4, positive_only=False))


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
    _game = _init_game()
    _g_PLAYER = 'player'
    _g_OPPONENT = 'opponent'
    
    @classmethod
    def _get_game(cls) -> PazaakGame:
        return cls._game

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request: HttpRequest) -> HttpResponse:
        print('GET - PlayView')
        PlayView._game = _init_game()

        move = cards.random_card(positive_only=True, bound=self._get_game().max_modifier)
        self._get_game().end_turn(self._get_game().player, move)

        context = {'player': self._get_game().player,
                   'opponent': self._get_game().opponent,
                   'player_move': move.modifier,
                   'status': 'start'}
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
        if self._get_game().game_over():
            return self._process_game_over()

        context = self._process_player_move(post_data)
        turn = context['turn']
        content = self._get_game().json()

        switch = {Turn.PLAYER.value: Turn.PLAYER, Turn.OPPONENT.value: Turn.OPPONENT}
        turn = switch[turn]
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
        turn = None

        # player ends turn - the opponent makes a move now
        if action == 'end-turn-player':
            status = 'play'
            turn = Turn.OPPONENT
            move = cards.random_card(positive_only=True, bound=self._get_game().max_modifier)
            self._get_game().end_turn(self._get_game().opponent, move)

        # opponent ends turn - the player makes a move now
        elif action == 'end-turn-opponent':
            status = 'play'
            turn = Turn.PLAYER
            move = cards.random_card(positive_only=True, bound=self._get_game().max_modifier)
            self._get_game().end_turn(self._get_game().player, move)

        elif action == 'hand-player':
            status = 'play'
            id_of_clicked_card = post_data['card']

        elif action == 'stand-player':
            self._get_game().player.stand()
            status = 'stand-player'

        else:
            pass

        context['status'] = status
        context['turn'] = turn.value
        return context


    def _process_game_over(self) -> dict:
        winner_code = self._get_game().winner()
        assert winner_code != self._get_game().GAME_ON, 'game is not over'
        switch = {
            self._get_game().PLAYER_WINS: 'player',
            self._get_game().OPPONENT_WINS: 'opponent',
            self._get_game().TIE: 'tie'
        }

        return {
            'status': 'game_over',
            'winner': switch[winner_code]
        }

    @staticmethod
    def _extract_card_id(card_id: str) -> int:
        pattern = '^card-[player|opponent]-hand-?P<index>(\w)$'
        match = re.match(pattern, card_id)