from server.serialization import Serializable


class Player(Serializable):
    def __init__(self, identifier: str, initial_characters: [str]):
        self._identifier = identifier
        self._characters = initial_characters


    def __repr__(self) -> str:
        return 'Player({0}, {1})'.format(self.id, self.characters)


    def __str__(self) -> str:
        return repr(self)


    @property
    def id(self) -> str:
        return self._identifier


    @property
    def characters(self) -> [str]:
        return self._characters


    def remove_character(self, index: int) -> None:
        character_length = len(self.characters)
        if not (0 <= index < character_length):
            raise IndexError('Expected an integer in the range [0, {0}); received {1}'.format(character_length, index))

        self._characters.pop(index)


    def context(self) -> dict:
        return {
            'id': self.id,
            'characters': self.characters
        }


if __name__ == '__main__':
    pass