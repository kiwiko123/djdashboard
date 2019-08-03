import inspect

from . import views
from pazaak.server.game import PazaakGameView
from server.url_tools import AutoParseableViewURL, url_patterns


app_name = 'pazaak'
_predicate = lambda cls: inspect.isclass(cls) and cls is not PazaakGameView and issubclass(cls, AutoParseableViewURL)
urlpatterns = url_patterns(views, predicate=_predicate)