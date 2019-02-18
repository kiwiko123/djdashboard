import enum
from pazaak.game.turn import Turn


class GameStatus(enum.Enum):
    PLAYER_WINS = 0
    OPPONENT_WINS = 1
    TIE = 2
    GAME_ON = 3

    def __bool__(self) -> bool:
        return self != self.GAME_ON

    @classmethod
    def from_turn(cls, turn: Turn):
        table = {
            Turn.PLAYER: cls.PLAYER_WINS,
            Turn.OPPONENT: cls.OPPONENT_WINS
        }

        if turn not in table:
            raise ValueError('unexpected Turn received ({0})'.format(turn))

        return table[turn]