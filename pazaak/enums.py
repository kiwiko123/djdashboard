import enum
import inspect
import pathlib
import sys

from server.serialization import SerializableEnum


# ======================================

@enum.unique
class Action(SerializableEnum):
    ACTION = 'action'
    END_TURN_PLAYER = 'end-turn-player'
    END_TURN_OPPONENT = 'end-turn-opponent'
    HAND_PLAYER = 'hand-player'
    STAND_PLAYER = 'stand-player'

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True

# ======================================

@enum.unique
class Player(SerializableEnum):
    PLAYER = 'player'
    OPPONENT = 'opponent'

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True

# ======================================

@enum.unique
class Turn(SerializableEnum):
    PLAYER = 'player'
    OPPONENT = 'opponent'

    @classmethod
    def opposite_turn(cls, turn) -> 'Turn':
        """
        Given a turn, returns the opposite player's Turn enum.
        """
        switch = {
            cls.PLAYER: cls.OPPONENT,
            cls.OPPONENT: cls.PLAYER
        }
        if turn not in switch:
            raise ValueError('{0} is not a valid Turn'.format(turn))
        return switch[turn]

# ======================================

@enum.unique
class GameStatus(SerializableEnum):
    PLAYER_WINS = 0
    OPPONENT_WINS = 1
    TIE = 2
    GAME_ON = 3
    PLAYER_FORFEIT = 4

    def __bool__(self) -> bool:
        return self != self.GAME_ON

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True

    @classmethod
    def from_turn(cls, turn: Turn):
        table = {
            Turn.PLAYER: cls.PLAYER_WINS,
            Turn.OPPONENT: cls.OPPONENT_WINS
        }

        if turn not in table:
            raise ValueError('unexpected Turn received ({0})'.format(turn))

        return table[turn]

    def key(self) -> str:
        return self.name.lower()

# ======================================

@enum.unique
class GameRule(SerializableEnum):
    MAX_CARDS_ON_TABLE = 9
    WINNING_SCORE = 20
    MAX_MODIFIER = 10

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True

# ======================================

@enum.unique
class Theme(SerializableEnum):
    LIGHT = 0
    DARK = 1

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True


if __name__ == '__main__':
    pass
