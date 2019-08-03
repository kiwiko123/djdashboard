import abc

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from scrabble.game.scrabble import ScrabbleGame

from server.url_tools import AutoParseableViewURL
from server.utilities import allow_cors, get_client_url, RequestType

from utilities.games import GameManager


_CLIENT_URL = get_client_url()


class ScrabbleGameManager(GameManager):
    def create_game(self):
        return ScrabbleGame(16, 16)


class ScrabbleGameView(View, AutoParseableViewURL, metaclass=abc.ABCMeta):
    game_manager = ScrabbleGameManager()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        The sole purpose of this override is to remove all CSRF requirements on requests.
        This may not be suitable if Pazaak is ever used in a production environment.
        """
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class NewGameView(ScrabbleGameView):

    @staticmethod
    def url() -> str:
        return '/api/new-game'

    @allow_cors(_CLIENT_URL, RequestType.GET)
    def get(self) -> HttpResponse:
        game_id = self.game_manager.new_game()
        context = {
            'gameId': game_id,
            'message': 'Success!'
        }
        return JsonResponse(context)


if __name__ == '__main__':
    pass