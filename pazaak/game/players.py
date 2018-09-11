from pazaak.game.cards import PazaakCard


class PazaakPlayer:
    def __init__(self, hand: [PazaakCard]):
        self._hand = hand
        self._score = 0
        self._is_standing = False
        self.placed = []

    @property
    def hand(self) -> [PazaakCard]:
        return self._hand

    @property
    def is_standing(self) -> bool:
        return self._is_standing

    @is_standing.setter
    def is_standing(self, new_status: bool) -> None:
        self._is_standing = new_status

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, new_score: int) -> None:
        self._score = new_score

    def stand(self) -> None:
        self.is_standing = True