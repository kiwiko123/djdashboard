from django.conf.urls import url
from . import views
from pazaak.server.url_tools import url_patterns


app_name = 'pazaak'
urlpatterns = []

try:
    urlpatterns = url_patterns(views)
except:
    urlpatterns = [
            url(r'^api/new-game/$', views.NewGameView.as_view(), name='new-game'),
            url(r'^api/end-turn/$', views.EndTurnView.as_view(), name='end-turn'),
        ]