import enum
import inspect
import pathlib
import sys

from pazaak.bases import SerializableEnum


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
class RequestType(enum.Enum):
    GET = 'GET'
    POST = 'POST'

# ======================================

@enum.unique
class Theme(SerializableEnum):
    LIGHT = 0
    DARK = 1

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True

# ======================================
# Helper Functions
# ======================================

def export_enums_to_js(write_file: pathlib.Path):
    """
    Automatically generate a JS class representing enums in this module.
    Generated enums must be derived from SerializableEnum,
    and must override the @classmethod should_export_to_js() to return True.

    Generation happens at server startup, in pazaak/apps.py.
    """
    enums_to_serialize = _get_classes_in_current_module(_should_serialize_to_js)
    with write_file.open('w') as outfile:
        header = [
            '// =========================',
            '// || AUTO-GENERATED FILE ||',
            '// ========================='
        ]

        outfile.write('\n'.join(header))
        outfile.write('\n\n')

        for enum_class in enums_to_serialize:
            _write_enum_as_js_class(enum_class, outfile)
            outfile.write('\n')


def _write_enum_as_js_class(cls: SerializableEnum, outfile: open) -> None:
    enum_name = cls.__name__
    if not cls.should_export_to_js():
        raise ValueError('override should_export_to_js() to return True'.format(enum_name))

    indentation = '    '
    body = ['{0}{1}: {2},'.format(indentation, e.name, _transform_enum_value(e)) for e in cls]
    lines = ['export const {0} = {{'.format(enum_name)] + body + ['};']
    for line in lines:
        outfile.write('{0}\n'.format(line))


def _should_serialize_to_js(member) -> bool:
    return member is not SerializableEnum \
       and issubclass(member, SerializableEnum) \
       and member.should_export_to_js()


def _transform_enum_value(enum_value: enum.Enum):
    """
    If the enum's value is a string, include quotes around it.
    """
    value = enum_value.value
    if type(value) is str:
        value = "'{0}'".format(value)
    return value


def _get_classes_in_current_module(predicate: callable) -> list:
    if __name__ not in sys.modules:
        raise ValueError("Couldn't find '{0}' in {1}".format(__name__, sys.modules))

    current_module = sys.modules[__name__]
    return [cls for _, cls in inspect.getmembers(current_module, lambda member: inspect.isclass(member) and predicate(member))]


if __name__ == '__main__':
    pass
