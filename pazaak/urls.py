import inspect

from . import views
from pazaak.server.game import PazaakGameView
from pazaak.server.url_tools import AutoParseableViewURL, url_patterns


app_name = 'pazaak'
urlpatterns = url_patterns(views)