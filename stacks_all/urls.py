from django.conf.urls import url
from django.http import HttpResponse
from stacks_all.models import Stacks
from stacks_category.models import StacksCategory





urlpatterns = [
    url(r'^all/(.+)/(.+)/$', Stacks.stacksAll),
    url(r'^create/(.+)/$', Stacks.creatStacks),
    url(r'^category/$', StacksCategory.categorys),
]
