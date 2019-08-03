import random
from scrabble.game.players import Player
from scrabble.game.words import WordChecker
from data_structures.matrices import ListMatrix



class ScrabbleMove:

    @classmethod
    def for_character(cls, player: Player, character: str, coordinate: (int,)):
        move = cls()
        move.player = player
        move.text = character
        move.coordinate = coordinate
        return move

    def __init__(self):
        self.player = None
        self.text = None
        self.coordinates = []
        self.coordinate = ()


class ScrabbleGame:
    _alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _max_characters_for_player = 8

    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_players=2):
        self._board = ListMatrix(number_of_rows, number_of_columns)
        self._word_checker = WordChecker()
        self._players = [self._create_player(s) for s in ('A', 'B')]
        self._index_of_current_player = 0


    def __str__(self) -> str:
        return str(self._board)


    def run(self) -> None:
        while not self.game_is_over():



    def game_is_over(self) -> bool:
        pass


    def _get_next_player(self) -> Player:
        modifier = 0 if self._index_of_current_player < len(self._players) else -1
        return self._players[self._index_of_current_player + modifier]


    def make_move(self, move: ScrabbleMove) -> bool:
        player = move.player
        word = move.text
        selected_coordinates = move.coordinates

        if len(word) != len(selected_coordinates):
            raise ValueError('Mismatched length between word "{0}" and coordinates {1}'.format(word, selected_coordinates))

        is_valid_move = self._is_valid_move(move)
        if is_valid_move:
            for character, coordinate in zip(word, selected_coordinates):
                self._board[coordinate] = ScrabbleMove.for_character(player, character, coordinate)

        return is_valid_move


    def _are_coordinates_valid(self, coordinates: [(int,)]) -> bool:
        return all(0 <= x < self._board.row_count() and 0 <= y < self._board.column_count() for x, y in coordinates)


    def _is_valid_move(self, move: ScrabbleMove) -> bool:
        player = move.player
        word = move.text
        coordinates = move.coordinates
        return self._are_coordinates_valid(coordinates) \
               and all(self._board.is_blank(row, column) for row, column in coordinates) \
               and self._word_checker.is_word(word)


    @classmethod
    def _get_random_character(cls) -> str:
        upper_bound = len(cls._alphabet)
        index = random.randrange(upper_bound)
        return cls._alphabet[index]


    @classmethod
    def _create_player(cls, id: str) -> Player:
        characters = [cls._get_random_character() for _ in range(cls._max_characters_for_player)]
        return Player(id, characters)


if __name__ == '__main__':
    pass