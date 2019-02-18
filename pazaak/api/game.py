import abc

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from pazaak.server.url_tools import ViewURLAutoParser
from pazaak.api.actions import Actions
from pazaak.game import cards
from pazaak.game.turn import Turn
from pazaak.game.game import PazaakGame, PazaakCard, GameOverError
from pazaak.helpers.utilities import allow_cors, serialize


def _init_game() -> PazaakGame:
    return PazaakGame(cards.random_cards(4, positive_only=False))


class PazaakGameAPI(generic.TemplateView, ViewURLAutoParser, metaclass=abc.ABCMeta):
    PLAYER_TAG = 'player'
    OPPONENT_TAG = 'opponent'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._game = _init_game()

    @property
    def game(self):
        return self._game

    def new_game(self):
        self._game = _init_game()
        return self.game

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    @method_decorator(allow_cors)
    def options(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse()


    def process_post(self, post_data: dict) -> dict:
        if 'winner' in post_data and post_data['winner']:
            return {
                'status': 'game-over',
                'winner': post_data['winner']
            }

        context = self._process_player_move(post_data)
        turn = context['turn']
        content = self.game.json()

        switch = {
            Turn.PLAYER.value: Turn.PLAYER,
            Turn.OPPONENT.value: Turn.OPPONENT
        }

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
        if action == Actions.END_TURN_PLAYER.value:
            context = self._next_move(Turn.OPPONENT)

        # opponent ends turn - the player makes a move now
        elif action == Actions.END_TURN_OPPONENT.value:
            context = self._next_move(Turn.PLAYER)

        elif action == Actions.HAND_PLAYER.value:
            card_index = post_data['card_index']
            assert card_index.isdigit(), 'expected numeric card index'
            card_index = int(card_index)
            move = self.game.choose_from_hand(self.game.player, card_index)
            context = self._next_move(Turn.PLAYER, move=move)

        elif action == Actions.STAND_PLAYER.value:
            self.game.player.is_standing = True
            context = self._next_move(Turn.PLAYER, make_move=False)

        else:
            context['error'] = 'Invalid response'

        return context


    def _next_move(self, turn: Turn, move=None) -> 'MoveInfo':
        player = None

        if turn == Turn.PLAYER:
            player = self.game.player
            if self.game.player.is_standing:
                move = PazaakCard.empty()
            elif move is None:
                move = cards.random_card(positive_only=True, bound=self.game.max_modifier)
        else:
            player = self.game.opponent
            move = self.game._get_opponent_move()

        context = {
            'status': 'play',
            'is_standing': player.is_standing,
            'turn': turn.value,
            'move': move,
            'winner': None
        }

        if move is not None:
            try:
                self.game.end_turn(turn, move)
            except GameOverError as e:
                context['winner'] = str(e)

        return serialize(**context)


    def _process_game_over(self) -> dict:
        winner_code = self.game.winner()
        assert winner_code != self.game.GAME_ON, 'game is not over'

        switch = {
            self.game.PLAYER_WINS: Turn.PLAYER.value,
            self.game.OPPONENT_WINS: Turn.OPPONENT.value,
            self.game.TIE: 'tie'
        }

        return {
            'status': 'game_over',
            'winner': switch[winner_code]
        }
