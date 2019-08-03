from server.serialization import Serializable


class Record(Serializable):
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def context(self) -> {str: int}:
        return {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties
        }


if __name__ == '__main__':
    pass