import random
import time
from pazaak.game import cards
from pazaak.game.cards import PazaakCard
from pazaak.errors import GameLogicError, GameOverError
from pazaak.game.players import PazaakPlayer
from pazaak.enums import GameRule, GameStatus, Turn
from pazaak.data_structures.hash_tables import MultiSet
from pazaak.bases import IntegerIdentifiable, Recordable
from pazaak.utilities.serialize import Serializable
from pazaak.utilities.functions import first_true


_HAND_SIZE = 4
_MAX_MODIFIER = GameRule.MAX_MODIFIER.value
_WINNING_SCORE = GameRule.WINNING_SCORE.value
_FILLED_TABLE_THRESHOLD = GameRule.MAX_CARDS_ON_TABLE.value


class PazaakGame(Serializable, IntegerIdentifiable, Recordable):
    def __init__(self, initial_pool: [PazaakCard], hand_size=_HAND_SIZE, max_modifier=_MAX_MODIFIER):
        Recordable.__init__(self)
        IntegerIdentifiable.__init__(self)
        self._hand_size = hand_size
        self._max_modifier = max_modifier

        opponent_cards = cards.random_cards(self._hand_size, positive_only=False, bound=5)
        opponent_hand = self._draw_hand(opponent_cards)
        player_hand = self._draw_hand(initial_pool)

        # making the opponent's hand a hash table adds some efficiency gain -- see self._get_opponent_move()
        self._opponent = PazaakPlayer(opponent_hand, Turn.OPPONENT.value, _hand_container_type=MultiSet)
        self._player = PazaakPlayer(player_hand, Turn.PLAYER.value)
        self._turn = Turn.PLAYER
        self._is_over = False


    @property
    def player(self) -> PazaakPlayer:
        return self._player


    @property
    def opponent(self) -> PazaakPlayer:
        return self._opponent


    @property
    def turn(self) -> Turn:
        return self._turn


    @property
    def is_over(self) -> bool:
        return self._is_over


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

        if player.is_standing or player.forfeited:
            status = self.winner()

        else:
            previous_score = player.score
            player.placed.append(move)
            new_score = player.score + move.modifier

            if new_score == _WINNING_SCORE:
                player.stand()

            # ending a turn with a score over 20 is an automatic loss
            if previous_score > _WINNING_SCORE and new_score > _WINNING_SCORE:
                status = GameStatus.from_turn(opposite_turn)
            else:
                player.score = new_score
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
        criteria = (self._forfeited, self._outscored, self._filled_table)
        invoker = lambda f: f()
        results = map(invoker, criteria)

        status = first_true(results, default=GameStatus.GAME_ON)
        self._is_over = status != GameStatus.GAME_ON

        self._update_records(status)

        return status


    def _forfeited(self) -> GameStatus:
        forfeited_player = first_true(self._players(), lambda player: player.forfeited)
        # for now, the only person that can forfeit is the player
        return GameStatus.GAME_ON if forfeited_player is None else GameStatus.PLAYER_FORFEIT


    def _outscored(self) -> GameStatus:
        """
        Determines if any player has won by outscore.
        Outscoring happens when both players are standing - the one with the highest score <= 20 wins.
        Returns the applicable GameStatus.
        """
        status = None

        if all(player.is_standing for player in self._players()):
            if self.player.score == self.opponent.score:
                status = GameStatus.TIE
            else:
                winning_player = max(self._players(), key=lambda player: (player.score <= _WINNING_SCORE, player.score))
                status = self._game_status_from_player(winning_player)

        else:
            status = GameStatus.GAME_ON

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
        return len(player.placed) >= _FILLED_TABLE_THRESHOLD and player.score <= _WINNING_SCORE


    def _update_records(self, status: GameStatus) -> None:
        if status == GameStatus.PLAYER_WINS:
            self.player.record.wins += 1
            self.opponent.record.losses += 1
        elif status in (GameStatus.OPPONENT_WINS, GameStatus.PLAYER_FORFEIT):
            self.player.record.losses += 1
            self.opponent.record.wins += 1
        elif status == GameStatus.TIE:
            self.player.record.ties += 1
            self.opponent.record.ties += 1


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
        """
        Prompts the player for their next move.
        Applies to the console-based game only.
        """
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
            self.player.forfeit()

        else:
            move = cards.random_card(positive_only=True, bound=self._max_modifier)

        return move


    def _get_opponent_move(self) -> PazaakCard:
        """
        Returns the opponent's next move.
        There's some limited intelligence here:
        1) if their score is higher than the player's score (but under 20), AND the player is standing,
           then the opponent will stand (causing the them to win).
        2) if the opponent has a card in their hand that, when played, will get their score to 20,
           then they'll play it.

        Otherwise, they'll just draw a random card.
        """
        card = None
        value_needed_to_win = _WINNING_SCORE - self.opponent.score
        card_needed_to_win = PazaakCard.empty() if value_needed_to_win == 0 else PazaakCard(_WINNING_SCORE - self.opponent.score)
        player_stood_too_early = self.player.is_standing and \
                                 ((self.player.score <= self.opponent.score <= _WINNING_SCORE) or \
                                  (self.player.score > _WINNING_SCORE and self.opponent.score <= _WINNING_SCORE))

        if self.opponent.score == _WINNING_SCORE or player_stood_too_early:
            self.opponent.stand()
            card = PazaakCard.empty()

        elif card_needed_to_win in self.opponent.hand:
            self.opponent.hand.remove(card_needed_to_win)
            card = card_needed_to_win

        elif self.opponent.score > _WINNING_SCORE:
            # if their score is over 20,
            # find a card from their hand that will maximize their score under 20
            card_needed = max(self.opponent.hand, key=lambda card: self.opponent.score + card.modifier <= _WINNING_SCORE)
            self.opponent.hand.remove(card_needed)
            card = card_needed

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



    def key(self) -> str:
        raise GameLogicError('PazaakGame object should not be a context key')


    def context(self) -> dict:
        return {
            Turn.PLAYER: self.player,
            Turn.OPPONENT: self.opponent,
        }


if __name__ == '__main__':
    pool = cards.random_cards(10, positive_only=False, bound=5)
    game = PazaakGame(pool)
    game.start()