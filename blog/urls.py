from django.conf.urls import url
from django.contrib import admin
import json

from django.http import HttpResponse
from blog.models import ResJson





urlpatterns = [
    url(r'^json/', ResJson.resJson),
]
