from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views import generic

import logging


logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# flick#web admin
admin_username = ''

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'flick/index.html'