from pazaak.game import cards
from pazaak.game.game import PazaakGame, PazaakCard, Turn, GameOverError
from pazaak.boiler.utilities import serialize


def _init_game() -> PazaakGame:
    return PazaakGame(cards.random_cards(4, positive_only=False))


class PazaakGameAPI:
    PLAYER_TAG = 'player'
    OPPONENT_TAG = 'opponent'
    _game = _init_game()

    @classmethod
    def game(cls) -> PazaakGame:
        return cls._game

    @classmethod
    def new_game(cls) -> PazaakGame:
        cls._game = _init_game()
        return cls.game()

    def process_post(self, post_data: dict) -> dict:
        if 'winner' in post_data and post_data['winner']:
            return {
                'status': 'game-over',
                'winner': post_data['winner']
            }

        context = self._process_player_move(post_data)
        turn = context['turn']
        content = self.game().json()

        switch = {Turn.PLAYER.value: Turn.PLAYER, Turn.OPPONENT.value: Turn.OPPONENT}
        turn = switch[turn]
        assert turn in content, 'expected turn to be one of ("player", "opponent")'
        context.update(content[turn])

        return context


    def _process_player_move(self, post_data: dict) -> dict:
        if 'action' not in post_data:
            return {}

        action = post_data['action']
        action = action.strip().lower()
        context = {}

        # player ends turn - the opponent makes a move now
        if action == 'end-turn-player':
            context = self._next_move(Turn.OPPONENT)

        # opponent ends turn - the player makes a move now
        elif action == 'end-turn-opponent':
            context = self._next_move(Turn.PLAYER)

        elif action == 'hand-player':
            card_index = post_data['card_index']
            assert card_index.isdigit(), 'expected numeric card index'
            card_index = int(card_index)
            move = self.game().player.hand.pop(card_index)
            context = self._next_move(Turn.PLAYER, move=move)

        elif action == 'stand-player':
            self.game().player.is_standing = True
            context = self._next_move(Turn.PLAYER, make_move=False)

        else:
            context['error'] = 'Invalid response'

        return context


    def _next_move(self, turn: Turn, move=None) -> 'MoveInfo':
        player = None

        if turn == Turn.PLAYER:
            player = self.game().player
            if self.game().player.is_standing:
                move = PazaakCard.empty()
            elif move is None:
                move = cards.random_card(positive_only=True, bound=self.game().max_modifier)
        else:
            player = self.game().opponent
            move = self.game()._get_opponent_move()

        context = {
            'status': 'play',
            'is_standing': player.is_standing,
            'turn': turn.value,
            'move': move,
            'winner': None
        }

        if move is not None:
            try:
                self.game().end_turn(turn, move)
            except GameOverError as e:
                context['winner'] = str(e)

        return serialize(**context)


    def _process_game_over(self) -> dict:
        winner_code = self.game().winner()
        assert winner_code != self.game().GAME_ON, 'game is not over'

        switch = {
            self.game().PLAYER_WINS: Turn.PLAYER.value,
            self.game().OPPONENT_WINS: Turn.OPPONENT.value,
            self.game().TIE: 'tie'
        }

        return {
            'status': 'game_over',
            'winner': switch[winner_code]
        }
