import abc

from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from pazaak.server.url_tools import AutoParseableViewURL
from pazaak.enums import Action, GameRule, GameStatus, Turn
from pazaak.game import cards
from pazaak.errors import GameLogicError, GameOverError, ServerError
from pazaak.game.game import PazaakGame, PazaakCard
from pazaak.bases import IntegerIdentifiable, serialize
from pazaak.utilities.contracts import expects


_MAX_MODIFIER = GameRule.MAX_MODIFIER.value

def _init_game() -> PazaakGame:
    return PazaakGame(cards.random_cards(4, positive_only=False, bound=5))


class GameManager(IntegerIdentifiable):
    def __init__(self):
        self._games = {}


    def new_game(self) -> int:
        game_id = self.new_id()
        game = _init_game()
        self._games[game_id] = game
        return game_id


    @expects(lambda self, game_id: game_id in self._games,
             exception=ServerError,
             message='Unknown game received')
    def get_game(self, game_id: int) -> PazaakGame:
        return self._games[game_id]


    def remove_game(self, game_id: int) -> None:
        if game_id in self._games:
            del self._games[game_id]


    def clean_games(self) -> None:
        games_to_remove = (game_id for game_id, game in self._games.items() if game.is_over)
        for game_id in games_to_remove:
            self.remove_game(game_id)


    def game_count(self) -> int:
        return len(self._games)


class PazaakGameView(View, AutoParseableViewURL, metaclass=abc.ABCMeta):
    """
    Intermediate class encapsulating common data for each View endpoint (in views.py).
    To support simultaneous games, PazaakGameView stores a static collection of all currently-ongoing games.
    Starting a new game generates a unique ID, which is persisted throughout all web requests made by the client.
    Upon receiving a request, the server verifies that the ID is valid, then retrieves the game mapped to that ID.
    One notable thing about this implementation is that separate browser tabs will have separate game instances.

    Each View must be derived from PazaakGameView to maintain state.
    """
    PLAYER_TAG = 'player'
    OPPONENT_TAG = 'opponent'
    game_manager = GameManager()


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        The sole purpose of this override is to remove all CSRF requirements on requests.
        This may not be suitable if Pazaak is ever used in a production environment.
        """
        return super().dispatch(request, *args, **kwargs)


    def process_post(self, payload: dict) -> dict:
        """
        Entry point for all View requests.
        The payload should always contain 2 things:
          1) the unique game ID.
          2) the action being taken.

        Based on the action, updates the state of the game and returns the relevant JSON response as a dictionary.
        """
        game = self._get_game_from_payload(payload)
        context = self._process_player_move(game, payload)
        content = game.json()
        turn = context['turn']['justWent']['value']
        if turn not in content:
            raise GameLogicError('expected turn to be one of ("player", "opponent")')

        context.update(content[turn])
        return context


    @expects(lambda self, game, payload: Action.ACTION.value in payload,
             exception=GameLogicError,
             message='did not receive "action" from payload')
    def _process_player_move(self, game: PazaakGame, payload: dict) -> dict:
        action = payload['action']
        action = action.strip().lower()
        turn = None
        move = PazaakCard.empty()

        # player ends turn - the opponent makes a move now
        if action == Action.END_TURN_PLAYER.value:
            turn = Turn.PLAYER

        # opponent ends turn - the player makes a move now
        elif action == Action.END_TURN_OPPONENT.value:
            turn = Turn.OPPONENT

        elif action == Action.HAND_PLAYER.value:
            card_index = payload['cardIndex']
            assert type(card_index) is int
            move = game.choose_from_hand(game.player, card_index)
            turn = Turn.PLAYER

        elif action == Action.STAND_PLAYER.value:
            game.player.stand()
            turn = Turn.PLAYER

        else:
            raise GameLogicError('invalid action "{0}" received from client'.format(action))

        return self._next_move(game, turn, move=move)


    def _next_move(self, game: PazaakGame, turn: Turn, move: PazaakCard) -> dict:
        player = None

        if turn == Turn.PLAYER:
            player = game.player
            if game.player.is_standing:
                move = PazaakCard.empty()
            elif not move:
                move = cards.random_card(positive_only=True, bound=_MAX_MODIFIER)

        elif turn == Turn.OPPONENT:
            player = game.opponent
            move = game._get_opponent_move()

        else:
            raise GameLogicError('invalid turn "{0}" received'.format(turn))

        context = {
            'status': GameStatus.GAME_ON.value,   # TODO fix in serialize()
            'move': move,
            'turn': {'justWent': game.turn},
        }

        if move is not None:
            try:
                context['status'] = game.end_turn(turn, move)
            except GameOverError as e:
                context['status'] = str(e)

        context['turn']['upNext'] = game.turn
        return serialize(context)


    @classmethod
    def _get_game_from_payload(cls, payload: dict) -> PazaakGame:
        key = 'gameId'
        if key not in payload:
            raise ValueError('Front-end did not send up a game ID')
        game_id = payload[key]
        return cls.game_manager.get_game(game_id)