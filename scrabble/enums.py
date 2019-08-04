import enum
from server.serialization import SerializableEnum


@enum.unique
class Player(SerializableEnum):
    PLAYER = 'player'
    OPPONENT = 'opponent'

    @classmethod
    def should_export_to_js(cls) -> bool:
        return True


if __name__ == '__main__':
    pass