import abc
from pazaak.errors import ServerError
from pazaak.utilities.contracts import expects
from utilities.identification import IntegerIncrementable


class GameManager(IntegerIncrementable, metaclass=abc.ABCMeta):

    def __init__(self):
        self._games = {}


    @abc.abstractmethod
    def create_game(self):
        pass


    def new_game(self) -> int:
        game_id = self.new_id()
        game = self.create_game()
        self._games[game_id] = game
        return game_id


    @expects(lambda self, game_id: game_id in self._games,
             exception=ServerError,
             message='Unknown game received')
    def get_game(self, game_id: int):
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