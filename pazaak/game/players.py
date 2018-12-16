from pazaak.game.cards import PazaakCard
from pazaak.boiler.bases import Serializable


class PazaakPlayer(Serializable):
    def __init__(self, hand: [PazaakCard], identifier: str, _hand_container_type=list):
        """
        Initialize a PazaakPlayer object.
        `hand` is a list of PazaakCards that the player will use as their hand deck.
        `identifier` is a string id - use `Turn.PLAYER.value` or `Turn.OPPONENT.value`.
        `_hand_container_type` can be used to change the data structure that represents the player's hand;
                               this is useful for efficiently choosing known card values for an 'intelligent opponent'.
        """
        self._hand = hand if _hand_container_type is list else _hand_container_type(hand)
        self._score = 0
        self._is_standing = False
        self.placed = []
        self._identifier = identifier

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

    @property
    def identifier(self) -> str:
        return self._identifier

    def json(self) -> dict:
        return {
            'hand': [card.parity() for card in self.hand],
            'placed': [card.parity() for card in self.placed],
            'score': self.score,
            'is_standing': self.is_standing,
            'identifier': self.identifier
        }


if __name__ == '__main__':
    pass