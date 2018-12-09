from django.conf.urls import url
from . import views

app_name = 'pazaak'
urlpatterns = [
        url(r'^api/new-game/$', views.NewGameView.as_view(), name='new-game'),
        url(r'^api/end-turn/$', views.EndTurnView.as_view(), name='end-turn'),
    ]