import random
from scrabble.game.players import Player
from scrabble.game.words import WordChecker
from data_structures.matrices import ListMatrix
from server.serialization import Serializable


class ScrabbleMove:

    @classmethod
    def for_character(cls, player: Player, character_index: int, coordinate: (int,)):
        move = cls()
        move.player = player
        move.character_index = character_index
        move.text = player.characters[character_index]
        move.coordinate = coordinate
        return move

    def __init__(self):
        self.player = None
        self.character_index = None
        self.text = None
        self.coordinates = []
        self.coordinate = ()


class ScrabbleGame(Serializable):
    _alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _max_characters_for_player = 8

    def __init__(self, number_of_rows: int, number_of_columns: int):
        self._board = ListMatrix(number_of_rows, number_of_columns)
        self._word_checker = WordChecker()
        self._player = self._create_player('Player')
        self._opponent = self._create_player('Opponent')
        self._index_of_current_player = 0


    def __str__(self) -> str:
        return str(self._board)


    @property
    def is_over(self) -> bool:
        return False


    def run(self) -> None:
        while not self.game_is_over():
            self._board.print()
            print()

            move = self._get_player_move()
            self.make_move(move)


    def game_is_over(self) -> bool:
        return self.is_over


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


    def _is_coordinate_valid(self, coordinate: (int,)) -> bool:
        x, y = coordinate
        return 0 <= x < self._board.row_count() and 0 <= y < self._board.column_count()


    def _are_coordinates_valid(self, coordinates: [(int,)]) -> bool:
        return all(self._is_coordinate_valid(coordinates) for coordinates in coordinates)


    def _is_valid_move(self, move: ScrabbleMove) -> bool:
        player = move.player
        word = move.text
        coordinates = move.coordinates
        return self._are_coordinates_valid(coordinates) \
               and all(self._board.is_blank(row, column) for row, column in coordinates) \
               and self._word_checker.is_word(word)


    def _get_player_move(self) -> ScrabbleMove:
        player = self._player
        character_index = self._get_player_character_index()
        row = self._get_player_move_coordinate(self._board.row_count(), 'row')
        column = self._get_player_move_coordinate(self._board.column_count(), 'column')

        return ScrabbleMove.for_character(player, character_index, (row, column))


    def _get_player_character_index(self) -> int:
        player = self._player
        character_index = -1
        while not (0 <= character_index < len(player.characters)):
            print(' '.join([character for character in player.characters]))
            print(' '.join([str(i + 1) for i in range(len(player.characters))]))
            player_input = input('Choose the index of the letter you\'d like to play: ').strip()
            if player_input.isdigit():
                character_index = int(player_input) - 1

        return character_index


    def _get_player_move_coordinate(self, upper_bound: int, prompt_word: str) -> int:
        result = -1

        while not (0 <= result < upper_bound):
            player_input = input('Enter the {0} you\'d like to play: '.format(prompt_word)).strip()
            if player_input.isdigit():
                result = int(player_input) - 1

        return result


    def _get_serializable_board(self) -> [list]:
        result = []
        for row_index, row in enumerate(self._board.rows()):
            row_result = [None if self._board.is_blank(row_index, column_index) else value for column_index, value in enumerate(row)]
            result.append(row_result)

        return result


    def context(self) -> dict:
        return {
            'board': self._board.rows(),
            'player': self._player,
            'opponent': self._opponent,
            'playerTiles': self._player.characters,
            'opponentTiles': self._opponent.characters
        }


    @classmethod
    def _get_random_character(cls) -> str:
        upper_bound = len(cls._alphabet)
        index = random.randrange(upper_bound)
        return cls._alphabet[index]


    @classmethod
    def _create_player(cls, id: str) -> Player:
        characters = [cls._get_random_character() for _ in range(cls._max_characters_for_player)]
        return Player(id, characters)


    def is_word(self, word: str) -> bool:
        return self._word_checker.is_word(word)


    def get_words_from_placed_tile(self, indices_by_coordinates: {(int,): int}) -> [str]:
        result = set()
        for coordinate, index in indices_by_coordinates.items():
            adjacent_words = self._find_adjacent_words(coordinate, indices_by_coordinates)
            result.update(adjacent_words)

        return result


    def _find_adjacent_words(self, coordinate: (int, int), indices_by_coordinates) -> [str]:
        right = self._find_adjacent_word(coordinate, indices_by_coordinates, 0, 1)
        down = self._find_adjacent_word(coordinate, indices_by_coordinates, 1, 0)

        result = {right, down}
        return {word for word in result if word is not None and self.is_word(word)}


    def _find_adjacent_word(self, coordinate: (int, int), indices_by_coordinates: {(int,): int}, row_delta: int, column_delta: int) -> str:
        result = ''
        directional_coordinate = tuple(coordinate)
        while self._is_coordinate_valid(directional_coordinate) \
                and (directional_coordinate in indices_by_coordinates or not self._board.is_blank(directional_coordinate[0], directional_coordinate[1])):
            if directional_coordinate not in indices_by_coordinates:
                return None

            index = indices_by_coordinates[directional_coordinate]
            result += self._player.characters[index]
            x, y = directional_coordinate
            directional_coordinate = (x + row_delta, y + column_delta)

        return result if result else None



if __name__ == '__main__':
    game = ScrabbleGame(10, 10)
    game.run()