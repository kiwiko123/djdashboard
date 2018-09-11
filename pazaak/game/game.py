import random
from pazaak.game import cards
from pazaak.game.cards import PazaakCard
from pazaak.game.players import PazaakPlayer


_HAND_SIZE = 4
_MAX_MODIFIER = 10

_PLAYER_FLAG = 0
_OPPONENT_FLAG = 1


class PazaakGame:

    PLAYER_WINS = 1
    OPPONENT_WINS = -1
    TIE = 0
    _WINNING_SCORE = 20

    def __init__(self, initial_pool: [PazaakCard], hand_size=_HAND_SIZE, max_modifier=_MAX_MODIFIER):
        self._initial_pool = initial_pool
        self._hand_size = hand_size
        self._max_modifier = max_modifier

        opponent_cards = cards.random_cards(self._hand_size, positive_only=False, bound=self._max_modifier)
        opponent_hand = self._draw_hand(opponent_cards)
        player_hand = self._draw_hand(self._initial_pool)

        self._opponent = PazaakPlayer(opponent_hand)
        self._player = PazaakPlayer(player_hand)

    @property
    def player(self) -> PazaakPlayer:
        return self._player

    @property
    def opponent(self) -> PazaakPlayer:
        return self._opponent

    @property
    def max_modifier(self) -> int:
        return self._max_modifier

    def start(self) -> None:
        self._print_game_status()

        while not self.game_over():
            player_move = self._get_player_move()
            self.make_move(self.player, player_move)
            self._print_game_status()

            opponent_move = self._get_opponent_move()
            self.make_move(self.opponent, opponent_move)
            self._print_game_status()


    def game_over(self) -> bool:
        return self.winner() is not None


    def winner(self) -> int:
        if self.player.is_standing and self.opponent.is_standing:
            winning_player = max([self.player, self.opponent], key=lambda p: (p.score < self._WINNING_SCORE, p.score))
            result = self.PLAYER_WINS if winning_player is self.player else self.OPPONENT_WINS
        elif self.opponent.score > self._WINNING_SCORE and self.player.score <= self._WINNING_SCORE:
            result = self.PLAYER_WINS
        elif self.player.score > self._WINNING_SCORE and self.opponent.score <= self._WINNING_SCORE:
            result = self.OPPONENT_WINS
        elif len(self.player.placed) >= 9 and self.player.score <= self._WINNING_SCORE:
            result = self.PLAYER_WINS
        elif len(self.opponent.placed) >= 9 and self.opponent.score <= self._WINNING_SCORE:
            result = self.OPPONENT_WINS
        elif self.player.score >= self._WINNING_SCORE and self.opponent.score >= self._WINNING_SCORE:
            result = self.TIE
        else:
            result = None
        # if self.player.score <= self._WINNING_SCORE and \
        #         (self.opponent.score > self._WINNING_SCORE or (self.opponent.score < self._WINNING_SCORE and self.opponent.is_standing)):
        #     result = self.PLAYER_WINS
        #
        # elif self.opponent.score <= self._WINNING_SCORE and \
        #         (self.player.score > self._WINNING_SCORE or (self.player.score < self._WINNING_SCORE and self.player.is_standing)):
        #     result = self.OPPONENT_WINS
        #
        # elif self.player.score >= self._WINNING_SCORE and self.opponent.score >= self._WINNING_SCORE:
        #     result = self.TIE
        #
        # else:
        #     result = None

        return result


    def _get_player_move(self) -> PazaakCard:
        if self.player.is_standing:
            return None

        response = input('[e]nd turn, [s]tand, or use a card from your hand [1-{0}]: '.format(len(self.player.hand)))
        response = response.upper()
        move = None

        if response.isnumeric():
            number = int(response)
            if 1 <= number <= len(self.player.hand):
                move = self.player.hand[number - 1]
                self.player.hand.pop(number - 1)
            else:
                print('Invalid number, choose again')
                return self._get_player_move()
        elif response == 'S':
            self.player.is_standing = True
        else:
            move = cards.random_card(positive_only=True, bound=self._max_modifier)

        return move


    def _get_opponent_move(self) -> PazaakCard:
        if self.opponent.is_standing:
            return None

        return cards.random_card(positive_only=True, bound=self._max_modifier)


    def make_move(self, player: PazaakPlayer, move: PazaakCard) -> None:
        if not player.is_standing:
            assert move is not None, 'expected PazaakCard; received `None`'
            player.placed.append(move)
            player.score += move.modifier


    def _print_game_status(self) -> None:
        print('You: {0}'.format(self._player.score))
        print('-' * 10)
        print(', '.join([card.parity() for card in self._player.placed]))
        print('-' * 10)
        print('| {0} |'.format(' | '.join([card.parity() for card in self._player.hand])))
        print('-' * 10)
        print()
        print('Opponent: {0}'.format(self._opponent.score))
        print('-' * 10)
        print(', '.join([card.parity() for card in self._opponent.placed]))
        print('-' * 10)
        print()

    def _draw_hand(self, pool: [PazaakCard]) -> [PazaakCard]:
        """
        Return a list of PazaakCards representing a player's "hand".
        A hand is a set of cards that the player can use instead of a random draw.
        Example - if the hand has a +3 card, and player's current score is 17,
        play the +3 card to make 20.
        """
        return random.sample(pool, self._hand_size)

    def json(self) -> dict:
        return {
            'player': {
                'score': self.player.score,
                'hand': [card.parity() for card in self.player.hand],
                'last_placed': self.player.placed[-1].parity() if self.player.placed else 0,
                'size': len(self.player.placed)
            },
            'opponent': {
                'score': self.opponent.score,
                'hand': [card.parity() for card in self.opponent.hand],
                'last_placed': self.opponent.placed[-1].parity() if self.opponent.placed else 0,
                'size': len(self.opponent.placed)
            }
        }


if __name__ == '__main__':
    pool = cards.random_cards(10, positive_only=False)
    game = PazaakGame(pool)
    game.start()