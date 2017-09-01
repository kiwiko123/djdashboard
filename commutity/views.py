from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def index(request: WSGIRequest) -> HttpResponse:
    return render(request, 'commutity/index.html')


def login(request: WSGIRequest) -> HttpResponse:
    return render(request, 'commutity/login.html')
