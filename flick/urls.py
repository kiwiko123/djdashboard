from django.conf.urls import url
from . import views

app_name = 'flick'
urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^login/$', views.LoginView.as_view(), name='login'),
        url(r'^create-acccount/$', views.CreateAccountView.as_view(), name='create-account'),
    ]