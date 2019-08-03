from . import views
from server.url_tools import is_auto_parseable, url_patterns


def _meets_auto_parse_criteria(member) -> bool:
    return is_auto_parseable(member) and member is not views.ScrabbleGameView


app_name = 'scrabble'
urlpatterns = url_patterns(views, predicate=_meets_auto_parse_criteria)
x = 0