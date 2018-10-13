import random


class PazaakCard:
    def __init__(self, modifier: int):
        """
        Initialize a new Pazaak card.
        Modifier is the value to add/subtract to the player's score.
        """
        self._modifier = modifier

    def __repr__(self) -> str:
        return '{0}({1})'.format(type(self).__name__, self.parity())

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: 'PazaakCard') -> bool:
        return isinstance(other, PazaakCard) and self.modifier == other.modifier

    @property
    def modifier(self) -> int:
        return self._modifier

    def parity(self) -> str:
        p = '+' if self.modifier > 0 else ''

        return '{0}{1}'.format(p, self.modifier)


def random_card(positive_only=True, bound=10) -> PazaakCard:
    lower_bound = 1 if positive_only else -bound
    return PazaakCard(random.randrange(lower_bound, bound + 1))


def random_cards(n: int, positive_only=True, bound=10) -> [PazaakCard]:
    """
    Returns `n` random Pazaak cards.

    `bound` is inclusive.
    """
    return [random_card(positive_only=positive_only, bound=bound) for _ in range(n)]