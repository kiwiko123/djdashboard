from pazaak.game.cards import PazaakCard
from pazaak.errors import GameLogicError
from pazaak.helpers.bases import Serializable, Trackable


class PazaakPlayer(Serializable, Trackable):
    def __init__(self, hand: [PazaakCard], identifier: str, _hand_container_type=list):
        """
        Initialize a PazaakPlayer object.
        `hand` is a list of PazaakCards that the player will use as their hand deck.
        `identifier` is a string id - use `Turn.PLAYER.value` or `Turn.OPPONENT.value`.
        `_hand_container_type` can be used to change the data structure that represents the player's hand;
                               this is useful for efficiently choosing known card values for an 'intelligent opponent'.
        """
        Trackable.__init__(self)
        self._hand = hand if _hand_container_type is list else _hand_container_type(hand)
        self._score = 0
        self._is_standing = False
        self._placed = []
        self._identifier = identifier
        self._forfeited = False

    def __str__(self) -> str:
        return 'PazaakPlayer({0})'.format(self.identifier)

    def __eq__(self, other) -> bool:
        return isinstance(other, PazaakPlayer) and self.identifier == other.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)

    @property
    def hand(self) -> [PazaakCard]:
        """
        The hand deck is the collection of cards that you can play instead of drawing a random card.
        These are useful when one of their values plus your current score equals 20.
        """
        return self._hand

    @property
    def placed(self) -> [PazaakCard]:
        """
        All of the cards this player has already placed.
        """
        return self._placed

    @property
    def is_standing(self) -> bool:
        """
        Once the player has stood, they cannot make any more moves until the game is over.
        """
        return self._is_standing

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, new_score: int) -> None:
        self._score = new_score

    @property
    def identifier(self) -> str:
        """
        "Friendly-name" identifier. Use Turn.PLAYER.value or Turn.OPPONENT.value.
        :return:
        """
        return self._identifier

    @property
    def forfeited(self) -> bool:
        return self._forfeited

    def stand(self) -> None:
        self._is_standing = True

    def forfeit(self) -> None:
        self._forfeited = True

    def key(self) -> str:
        raise GameLogicError('PazaakPlayer should not be a context key')

    def context(self) -> dict:
        return {
            'hand': list(self.hand),
            'placed': self.placed,
            'score': self.score,
            'isStanding': self.is_standing,
            'identifier': self.identifier
        }


if __name__ == '__main__':
    pass