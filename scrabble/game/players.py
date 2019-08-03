


class Player:
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


if __name__ == '__main__':
    pass