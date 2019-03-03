import random
import time
from pazaak.game import cards
from pazaak.game.cards import PazaakCard
from pazaak.game.errors import GameLogicError, GameOverError
from pazaak.game.players import PazaakPlayer
from pazaak.enums import GameStatus, Turn
from pazaak.data_structures.hash_tables import MultiSet
from pazaak.helpers.bases import Serializable
from pazaak.helpers.utilities import first_true


_HAND_SIZE = 4
_MAX_MODIFIER = 10


class PazaakGame(Serializable):
    _WINNING_SCORE = 20
    _FILLED_TABLE_THRESHOLD = 9     # the number of cards a player has placed before winning by filling the table

    def __init__(self, initial_pool: [PazaakCard], hand_size=_HAND_SIZE, max_modifier=_MAX_MODIFIER):
        self._initial_pool = initial_pool
        self._hand_size = hand_size
        self._max_modifier = max_modifier

        opponent_cards = cards.random_cards(self._hand_size, positive_only=False, bound=self._max_modifier)
        opponent_hand = self._draw_hand(opponent_cards)
        player_hand = self._draw_hand(self._initial_pool)

        # making the opponent's hand a hash table adds some efficiency gain -- see self._get_opponent_move()
        self._opponent = PazaakPlayer(opponent_hand, Turn.OPPONENT.value, _hand_container_type=MultiSet)
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


    def _players(self) -> (PazaakPlayer,):
        """
        Returns a tuple of the players in the game.
        """
        return (self.player, self.opponent)


    def _game_status_from_player(self, player: PazaakPlayer) -> GameStatus:
        """
        Given a player, return the GameStatus corresponding to them.
        """
        table = {
            self.player: GameStatus.PLAYER_WINS,
            self.opponent: GameStatus.OPPONENT_WINS
        }

        if player not in table:
            raise ValueError('received unexpected player {0}'.format(player))

        return table[player]


    def start(self) -> None:
        """
        Begins a console-based version of Pazaak.
        The player goes first.
        """
        self._print_player_game(self.player)
        self._print_player_game(self.opponent)
        status = GameStatus.GAME_ON
        switch = {
            Turn.PLAYER: self.player,
            Turn.OPPONENT: self.opponent
        }

        while not status:
            try:
                turn = self._turn
                current_player = switch[turn]
                move = self._get_move(current_player)
                status = self.end_turn(turn, move)
                self._print_player_game(current_player, show_hand=True)
                time.sleep(0.5)

            except GameOverError as e:
                status = str(e)
                break

        if not status:
            status = self.winner()
        print('Winner: {0}!'.format(status))


    def end_turn(self, turn: Turn, move: PazaakCard) -> GameStatus:
        """
        Given a turn and a move, updates the game for the specified player.
        If the player is already standing, no move will be made.
        Automatically switches self._turn.
        Calculates and returns the game's updated status.
        """
        switch = {
            Turn.PLAYER: self.player,
            Turn.OPPONENT: self.opponent
        }
        player = switch[turn]
        opposite_turn = Turn.opposite_turn(self._turn)
        status = GameStatus.GAME_ON

        if player.is_standing:
            status = self.winner()

        else:
            previous_score = player.score
            player.placed.append(move)
            player.score += move.modifier

            if player.score == self._WINNING_SCORE:
                player.stand()

            # ending a turn with a score over 20 is an automatic loss
            if previous_score > self._WINNING_SCORE:
                status = GameStatus.from_turn(opposite_turn)
            else:
                status = self.winner()

        self._turn = opposite_turn
        return status


    def choose_from_hand(self, player: PazaakPlayer, card_index: int) -> PazaakCard:
        """
        Chooses and returns the index of the card from the player's hand.
        Removes that card from the player's hand.
        Note that card_index is expected to be 0-based, but will 1-based from the player's UI.
        """
        container_type = type(player.hand)
        if not hasattr(container_type, 'pop'):
            raise GameLogicError('custom hand container type {0} for {1} has no "pop" method'.format(container_type, player))

        if card_index > len(player.hand):
            raise GameLogicError('hand-card index {0} out of bounds for {1}'.format(card_index, player))

        return player.hand.pop(card_index)


    def winner(self) -> GameStatus:
        outscored = self._outscored()
        filled_table = self._filled_table()

        results = (outscored, filled_table)
        return first_true(results, default=GameStatus.GAME_ON)


    def _forfeited(self) -> GameStatus:
        pass


    def _outscored(self) -> GameStatus:
        """
        Determines if any player has won by outscore.
        Outscoring happens when both players are standing - the one with the highest score <= 20 wins.
        Returns the applicable GameStatus.
        """
        status = None
        if not all(player.is_standing for player in self._players()):
            # if no one is standing yet, then continue the game
            status = GameStatus.GAME_ON

        elif self.player.score == self.opponent.score:
            status = GameStatus.TIE

        else:
            winning_player = max(self._players(), key=lambda player: (player.score <= self._WINNING_SCORE, player.score))
            status = self._game_status_from_player(winning_player)

        return status


    def _filled_table(self) -> GameStatus:
        """
        Determines if any player has won by filling the table.
        Filling the table happens when has placed 9 cards without going bust, and still has a score under 20.
        This is an automatic win.
        Returns the applicable GameStatus.
        :return:
        """
        results = {self._game_status_from_player(player): self._player_filled_table(player) for player in self._players()}
        return first_true(results, predicate=lambda status: results[status], default=GameStatus.GAME_ON)


    def _player_filled_table(self, player: PazaakPlayer) -> bool:
        return len(player.placed) >= self._FILLED_TABLE_THRESHOLD and player.score <= self._WINNING_SCORE


    def _get_move(self, player: PazaakPlayer) -> PazaakCard:
        if player.is_standing:
            return PazaakCard.empty()

        table = {
            self.player: self._get_player_move,
            self.opponent: self._get_opponent_move
        }

        if player not in table:
            raise ValueError('received unexpected player {0}'.format(player))

        method = table[player]
        return method()


    def _get_player_move(self) -> PazaakCard:
        prompt = ''
        if self.player.hand:
            cards_in_hand = len(self.player.hand)
            range = str(cards_in_hand) if cards_in_hand == 1 else '1-{0}'.format(cards_in_hand)
            prompt = '[e]nd turn, [s]tand, or use a card from your hand [{0}]: '.format(range)
        else:
            prompt = '[e]nd turn or [s]tand: '

        response = input(prompt)
        response = response.strip().upper()
        move = PazaakCard.empty()

        if response.isnumeric():
            number = int(response)
            if 1 <= number <= len(self.player.hand):
                move = self.choose_from_hand(self.player, number - 1)
            else:
                print('Invalid number, choose again')
                return self._get_player_move()

        elif response == 'S':
            self.player.stand()

        elif response == 'Q':
            raise GameOverError('Player forfeited the game')

        else:
            move = cards.random_card(positive_only=True, bound=self._max_modifier)

        return move


    def _get_opponent_move(self) -> PazaakCard:
        card = None
        value_needed_to_win = self._WINNING_SCORE - self.opponent.score
        card_needed_to_win = PazaakCard.empty() if value_needed_to_win == 0 else PazaakCard(self._WINNING_SCORE - self.opponent.score)

        if self.opponent.score == self._WINNING_SCORE or \
           (self.player.is_standing and self.player.score < self.opponent.score <= self._WINNING_SCORE):
            self.opponent.stand()
            card = PazaakCard.empty()

        elif card_needed_to_win in self.opponent.hand:
            self.opponent.hand.remove(card_needed_to_win)
            card = card_needed_to_win

        else:
            card = cards.random_card(positive_only=True, bound=self._max_modifier)

        return card


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


    def _is_tied(self) -> bool:
        return (self.player.score == self._WINNING_SCORE and self.player.score == self.opponent.score) or \
               (self.player.score > self._WINNING_SCORE and self.opponent.score > self._WINNING_SCORE)


    def key(self) -> str:
        raise GameLogicError('PazaakGame object should not be a context key')


    def context(self) -> dict:
        return {
            Turn.PLAYER: {
                'score': self.player.score,
                'hand': self.player.hand,
                'placed': self.player.placed,
                # 'last_placed': self.player.placed[-1].parity() if self.player.placed else 0,
                'size': len(self.player.placed),
                'isStanding': self.player.is_standing
            },
            Turn.OPPONENT: {
                'score': self.opponent.score,
                'hand': list(self.opponent.hand),
                'placed': self.opponent.placed,
                # 'last_placed': self.opponent.placed[-1].parity() if self.opponent.placed else 0,
                'size': len(self.opponent.placed),
                'isStanding': self.opponent.is_standing
            }
        }


if __name__ == '__main__':
    pool = cards.random_cards(10, positive_only=False, bound=5)
    game = PazaakGame(pool)
    game.start()