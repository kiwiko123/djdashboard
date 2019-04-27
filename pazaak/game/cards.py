import random

from pazaak.errors import GameLogicError
from pazaak.bases import IntegerIdentifiable, Serializable
from pazaak.utilities.contracts import expects
from pazaak.utilities.functions import coin_flip


class PazaakCard(Serializable, IntegerIdentifiable):
    __EMPTY_VALUE = 0
    __initializing_empty = False

    @classmethod
    def empty(cls) -> 'PazaakCard':
        """
        Returns an "empty" Pazaak card.
        This is useful for representing a non-playable Pazaak card, without having to use None.
        It's initialized with a value of 0 -- PazaakCards can't otherwise be initialized with this value (outside of this method).
        """
        cls.__initializing_empty = True
        card = cls(cls.__EMPTY_VALUE)
        cls.__initializing_empty = False
        return card

    @expects(lambda self, modifier: modifier != PazaakCard.__EMPTY_VALUE or PazaakCard.__initializing_empty,
             exception=ValueError,
             message='cannot initialize a PazaakCard with the empty card value')
    def __init__(self, modifier: int):
        """
        Initialize a new Pazaak card.
        Modifier is the value to add/subtract to the player's score.
        Cannot be initialized with a value of 0.
        """
        super().__init__()
        self._modifier = modifier

    def __repr__(self) -> str:
        return '{0}({1})'.format(type(self).__name__, self.parity())

    def __str__(self) -> str:
        return repr(self)

    def __bool__(self) -> bool:
        return self != PazaakCard.empty()

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: 'PazaakCard') -> bool:
        return isinstance(other, PazaakCard) and self.modifier == other.modifier

    @property
    def modifier(self) -> int:
        """
        The value of the card.
        """
        return self._modifier

    def parity(self) -> str:
        """
        A string representing the value of the card, with it's "sign" in front of it.
        Example: "+5"
        """
        p = '+' if self.modifier > 0 else ''
        return '{0}{1}'.format(p, self.modifier)

    def key(self) -> str:
        raise GameLogicError('PazaakCard should not be a context key')

    def context(self) -> dict:
        return {
            'modifier': self.modifier,
            'parity': self.parity()
        }


def random_card(positive_only=True, bound=10) -> PazaakCard:
    """
    Returns a random card within the provided bound.
    If positive_only=True, the range is [1, bound].
    If not, the range is [-bound, -1] U [1, bound].
    """
    value = None
    if positive_only:
        value = random.randrange(1, bound + 1)
    else:
        negative_value = random.randrange(-bound, 0)
        positive_value = random.randrange(1, bound + 1)
        value = positive_value if coin_flip() else negative_value

    return PazaakCard(value)


def random_cards(n: int, positive_only=True, bound=10) -> [PazaakCard]:
    """
    Returns `n` random Pazaak cards.

    `bound` is inclusive.
    """
    return [random_card(positive_only=positive_only, bound=bound) for _ in range(n)]