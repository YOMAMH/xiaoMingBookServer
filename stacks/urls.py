from django.conf.urls import url
from django.http import HttpResponse
from stacks.models import Stacks





urlpatterns = [
    url(r'^all/(.+)/$', Stacks.stacksAll),
    url(r'^create/', Stacks.creatStacks),
]
