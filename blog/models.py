from django.db import models
from django.utils import timezone
from django.http import HttpResponse, request
import json


class ResJson(models.Model):
    author = models.TextField()
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def pushDate(self):
        self.published_date = timezone.now()
        self.save()

    def resJson(self):
        resObj = ResJson.objects.get(id = 1)
        ObjTem = {
            'author' : resObj.author,
            'title' : resObj.title,
            'text' : resObj.text,
        }
        jsonStr = json.dumps(ObjTem)
        response = HttpResponse(jsonStr)
        return response

