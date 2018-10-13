from django.conf.urls import url
from . import views

app_name = 'pazaak'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^play/$', views.PlayView.as_view(), name='play')
    ]