import enum
import random
import time
from pazaak.game import cards
from pazaak.game.cards import PazaakCard
from pazaak.game.players import PazaakPlayer
from pazaak.game.data_structures.hash_tables import MultiSet
from pazaak.boiler.bases import Serializable


_HAND_SIZE = 4
_MAX_MODIFIER = 10


class Turn(enum.Enum):
    PLAYER = 'player'
    OPPONENT = 'opponent'


class GameOverError(Exception):
    pass


class PazaakGame(Serializable):
    GAME_ON = 0
    PLAYER_WINS = Turn.PLAYER.value
    OPPONENT_WINS = Turn.OPPONENT.value
    TIE = 'tie'
    _WINNING_SCORE = 20

    _turn_switch = {
        Turn.PLAYER: Turn.OPPONENT,
        Turn.OPPONENT: Turn.PLAYER
    }

    def __init__(self, initial_pool: [PazaakCard], hand_size=_HAND_SIZE, max_modifier=_MAX_MODIFIER):
        self._initial_pool = initial_pool
        self._hand_size = hand_size
        self._max_modifier = max_modifier

        opponent_cards = cards.random_cards(self._hand_size, positive_only=True, bound=self._max_modifier)
        opponent_hand = self._draw_hand(opponent_cards)
        player_hand = self._draw_hand(self._initial_pool)

        self._opponent = PazaakPlayer(opponent_hand, Turn.OPPONENT.value, MultiSet)
        self._player = PazaakPlayer(player_hand, Turn.PLAYER.value)
        self._turn = Turn.PLAYER

    @property
    def player(self) -> PazaakPlayer:
        return self._player

    @property
    def opponent(self) -> PazaakPlayer:
        return self._opponent

    @property
    def max_modifier(self) -> int:
        return self._max_modifier

    @property
    def turn(self) -> Turn:
        return self._turn

    @classmethod
    def _other_turn(cls, player: PazaakPlayer) -> Turn:
        return cls._turn_switch[player]

    def _other_player(self, player: PazaakPlayer) -> PazaakPlayer:
        return self.player if player == self.opponent else self.opponent


    def start(self) -> None:
        winner = ''
        self._print_player_game(self.player)
        self._print_player_game(self.opponent)

        while not self.game_over():
            try:
                player_move = self._get_player_move()
                self.end_turn(Turn.PLAYER, player_move)
                self._print_player_game(self.player)

                opponent_move = self._get_opponent_move()
                self.end_turn(Turn.OPPONENT, opponent_move)
                self._print_player_game(self.opponent, show_hand=True)
                time.sleep(0.5)

            except GameOverError as e:
                winner = str(e)
                break

        if not winner:
            winner = self.winner()
        print('Winner: {0}!'.format(winner))


    def _game_over(self, player: PazaakPlayer) -> bool:
        conditions = (
            player.score > self._WINNING_SCORE,
            self.winner() != self.GAME_ON,
        )
        return any(conditions)


    def winner(self) -> int:
        # return early for efficiency
        if all(not player.is_standing and player.score < self._WINNING_SCORE for player in (self.player, self.opponent)):
            return self.GAME_ON

        elif self._is_tied():
            result = self.TIE

        # outscore: if both players are standing, the player with the highest score <= 20 wins
        elif self.player.is_standing and self.opponent.is_standing:
            winning_player = max([self.player, self.opponent], key=lambda p: (p.score <= self._WINNING_SCORE, p.score))
            result = self.PLAYER_WINS if winning_player is self.player else self.OPPONENT_WINS

        # filling the table: placing 9 cards without busting is an automatic win
        elif self._filled_table(self.player):
            result = self.PLAYER_WINS

        elif self._filled_table(self.opponent):
            result = self.OPPONENT_WINS

        else:
            result = self.GAME_ON

        return result


    def _get_player_move(self) -> PazaakCard:
        if self.player.is_standing:
            return None

        response = input('[e]nd turn, [s]tand, or use a card from your hand [1-{0}]: '.format(len(self.player.hand)))
        response = response.strip().upper()
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
            return PazaakCard.empty()

        if self.opponent.score == self._WINNING_SCORE or \
           (self.player.is_standing and self.player.score < self.opponent.score <= self._WINNING_SCORE):
            self.opponent.is_standing = True
            return PazaakCard.empty()

        needed = PazaakCard(self._WINNING_SCORE - self.opponent.score)
        if needed in self.opponent.hand:
            self.opponent.hand.remove(needed)
            return needed

        return cards.random_card(positive_only=True, bound=self._max_modifier)


    def end_turn(self, turn: Turn, move: PazaakCard) -> None:
        switch = {
            Turn.PLAYER: self.player,
            Turn.OPPONENT: self.opponent
        }
        player = switch[turn]

        if player.is_standing:
            winner = self.winner()
            if winner != self.GAME_ON:
                raise GameOverError(winner)

        else:
            assert move is not None, 'expected PazaakCard; received `None`'
            player.placed.append(move)
            player.score += move.modifier
            self._turn = self._other_turn(self.turn)

            if player.score == self._WINNING_SCORE:
                player.is_standing = True

            # ending a turn with a score over 20 is an automatic loss
            ended_turn_over_twenty = player.score > self._WINNING_SCORE
            winner = self.winner()
            if ended_turn_over_twenty or winner != self.GAME_ON:
                raise GameOverError(self._turn.value if ended_turn_over_twenty else winner)


    def _print_player_game(self, player: PazaakPlayer, show_hand=True) -> None:
        hand_repr = '| {0} |'.format(' | '.join([card.parity() if show_hand else 'X' for card in player.hand]))
        divider_size = len(hand_repr)
        pronoun = 'You' if player is self.player else 'Opponent'
        print('{0}: {1}'.format(pronoun, player.score))

        if not player.is_standing:
            print('-' * divider_size)
            print(', '.join([card.parity() for card in player.placed]))
            print('-' * divider_size)
            print(hand_repr)
            print('-' * divider_size)

        print()

    def _draw_hand(self, pool: [PazaakCard]) -> [PazaakCard]:
        """
        Return a list of PazaakCards representing a player's "hand".
        A hand is a set of cards that the player can use instead of a random draw.
        Example - if the hand has a +3 card, and player's current score is 17,
        play the +3 card to make 20.
        """
        return random.sample(pool, self._hand_size)

    @classmethod
    def _filled_table(cls, player: PazaakPlayer) -> bool:
        return len(player.placed) >= 9 and player.score <= cls._WINNING_SCORE


    def _is_tied(self) -> bool:
        return (self.player.score == self._WINNING_SCORE and self.player.score == self.opponent.score) or \
               (self.player.score > self._WINNING_SCORE and self.opponent.score > self._WINNING_SCORE)


    def json(self) -> dict:
        return {
            Turn.PLAYER: {
                'score': self.player.score,
                'hand': [card.parity() for card in self.player.hand],
                # 'last_placed': self.player.placed[-1].parity() if self.player.placed else 0,
                'size': len(self.player.placed),
                'is_standing': self.player.is_standing
            },
            Turn.OPPONENT: {
                'score': self.opponent.score,
                'hand': [card.parity() for card in self.opponent.hand],
                # 'last_placed': self.opponent.placed[-1].parity() if self.opponent.placed else 0,
                'size': len(self.opponent.placed),
                'is_standing': self.opponent.is_standing
            }
        }


if __name__ == '__main__':
    pool = cards.random_cards(10, positive_only=False, bound=5)
    game = PazaakGame(pool)
    game.start()