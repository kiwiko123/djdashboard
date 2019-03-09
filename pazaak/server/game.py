import abc

from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from pazaak.server.url_tools import AutoParseableViewURL
from pazaak.enums import Actions, GameRules, GameStatus, Turn
from pazaak.game import cards
from pazaak.errors import GameLogicError, GameOverError, ServerError
from pazaak.game.game import PazaakGame, PazaakCard
from pazaak.helpers.bases import serialize


_MAX_MODIFIER = GameRules.MAX_MODIFIER.value

def _init_game() -> PazaakGame:
    return PazaakGame(cards.random_cards(4, positive_only=False, bound=5))



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
    _games = {}
    _game_id = 0


    @classmethod
    def retrieve_game(cls, game_id: int) -> PazaakGame:
        """
        Returns the game associated with the given ID.
        """
        if game_id not in cls._games:
            raise ServerError('Unknown game received')
        return cls._games[game_id]


    @classmethod
    def new_game(cls) -> None:
        """
        Creates a new game and returns the generated ID associated to it.
        """
        new_game_id = cls._post_increment_game_id()
        cls._games[new_game_id] = _init_game()
        return new_game_id


    @classmethod
    def remove_game(cls, game_id: int) -> None:
        """
        Deletes the game associated to the given ID.
        Call this when manually starting a game over.
        """
        if game_id in cls._games:
            del cls._games[game_id]


    @classmethod
    def _post_increment_game_id(cls) -> int:
        """
        Generates and returns a new game ID.
        """
        game_id = cls._game_id
        cls._game_id += 1
        return game_id


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


    def _process_player_move(self, game: PazaakGame, payload: dict) -> dict:
        if Actions.ACTION.value not in payload:
            raise GameLogicError('did not receive "action" from payload')

        action = payload['action']
        action = action.strip().lower()
        turn = None
        move = None

        # player ends turn - the opponent makes a move now
        if action == Actions.END_TURN_PLAYER.value:
            turn = Turn.PLAYER

        # opponent ends turn - the player makes a move now
        elif action == Actions.END_TURN_OPPONENT.value:
            turn = Turn.OPPONENT

        elif action == Actions.HAND_PLAYER.value:
            card_index = payload['cardIndex']
            assert type(card_index) is int
            move = game.choose_from_hand(game.player, card_index)
            turn = Turn.PLAYER

        elif action == Actions.STAND_PLAYER.value:
            game.player.stand()
            turn = Turn.PLAYER

        else:
            raise GameLogicError('invalid action "{0}" received from client'.format(action))

        return self._next_move(game, turn, move=move)


    def _next_move(self, game: PazaakGame, turn: Turn, move=None) -> 'MoveInfo':
        player = None

        if turn == Turn.PLAYER:
            player = game.player
            if game.player.is_standing:
                move = PazaakCard.empty()
            elif move is None:
                move = cards.random_card(positive_only=True, bound=_MAX_MODIFIER)

        elif turn == Turn.OPPONENT:
            player = game.opponent
            move = game._get_opponent_move()

        else:
            raise GameLogicError('invalid turn "{0}" received'.format(turn))

        context = {
            'status': GameStatus.GAME_ON.value,   # TODO fix in serialize()
            'move': move,
            'turn': {'justWent': game.turn}
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
        return cls.retrieve_game(game_id)