import abc

from pazaak.errors import ServerError
from pazaak.utilities.contracts import expects
from utilities.identification import IntegerIncrementor, Recordable


class _GameData(Recordable):
    def __init__(self, game):
        Recordable.__init__(self)
        self.game = game

    def __str__(self) -> str:
        return '_GameData({0})'.format(self.game)


class GameManager(metaclass=abc.ABCMeta):
    def __init__(self):
        self._games = {}


    @abc.abstractmethod
    def create_game(self):
        pass


    def new_game(self) -> int:
        game_id = IntegerIncrementor.new_id()
        game = self.create_game()
        self._games[game_id] = _GameData(game)
        return game_id


    @expects(lambda self, game_id: game_id in self._games,
             exception=ServerError,
             message='Unknown game received')
    def get_game(self, game_id: int):
        return self._games[game_id].game


    def get_game_from_payload(self, payload: dict, key='gameId'):
        if key not in payload:
            raise KeyError('Did not find a gameId key in payload: "{0}"'.format(payload))
        return payload[key]


    def remove_game(self, game_id: int) -> None:
        if game_id in self._games:
            del self._games[game_id]


    def clean_games(self) -> None:
        games_to_remove = (game_id for game_id, game in self._games.items())
        for game_id in games_to_remove:
            self.remove_game(game_id)


    def clean_games_by_created_time(self, max_entries_to_remove: int, oldest_first=True) -> None:
        if max_entries_to_remove <= self.game_count():
            return

        games_ordered_by_created_time = sorted(self._games, key=lambda game_id: self._games[game_id].created_time, reverse=not oldest_first)
        for game_id in games_ordered_by_created_time[:max_entries_to_remove]:
            self.remove_game(game_id)


    def game_count(self) -> int:
        return len(self._games)