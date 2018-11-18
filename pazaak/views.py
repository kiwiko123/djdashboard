from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import collections
import re

from .game import cards
from .game.cards import PazaakCard
from .game.game import PazaakGame, Turn, GameOverError


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

    @classmethod
    def _move(cls, **fields):
        field_decl = ['status', 'turn', 'is_standing', 'move', 'winner']
        MoveInfo = collections.namedtuple('MoveInfo', field_decl)
        return MoveInfo(**fields)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request: HttpRequest) -> HttpResponse:
        print('GET - PlayView')
        PlayView._game = _init_game()

        move = cards.random_card(positive_only=True, bound=self._get_game().max_modifier)
        self._get_game().end_turn(Turn.PLAYER, move)

        context = {'player': self._get_game().player,
                   'opponent': self._get_game().opponent,
                   'move': move.modifier,
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
        if 'winner' in post_data and post_data['winner']:
            return {
                'status': 'game-over',
                'winner': post_data['winner']
            }

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

        # player ends turn - the opponent makes a move now
        if action == 'end-turn-player':
            payload = self._next_move(Turn.OPPONENT)
            context = payload._asdict()

        # opponent ends turn - the player makes a move now
        elif action == 'end-turn-opponent':
            payload = self._next_move(Turn.PLAYER)
            context = payload._asdict()

        elif action == 'hand-player':
            card_index = post_data['card_index']
            assert card_index.isdigit(), 'expected numeric card index'
            card_index = int(card_index)
            move = self._get_game().player.hand.pop(card_index)
            payload = self._next_move(Turn.PLAYER, move=move)
            context = payload._asdict()

        elif action == 'stand-player':
            self._get_game().player.is_standing = True
            payload = self._next_move(Turn.PLAYER, make_move=False)
            context = payload._asdict()

        else:
            context['error'] = 'Invalid response'

        return context


    def _next_move(self, turn: Turn, move=None) -> 'MoveInfo':
        player = None

        if turn == Turn.PLAYER:
            player = self._get_game().player
            if self._get_game().player.is_standing:
                move = PazaakCard.empty()
            elif move is None:
                move = cards.random_card(positive_only=True, bound=self._get_game().max_modifier)
        else:
            player = self._get_game().opponent
            move = self._get_game()._get_opponent_move()

        context = {
            'status': 'play',
            'is_standing': player.is_standing,
            'turn': turn.value,
            'move': move.modifier,
            'winner': None
        }

        if move is not None:
            try:
                self._get_game().end_turn(turn, move)
            except GameOverError as e:
                context['winner'] = str(e)

        return self._move(**context)


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