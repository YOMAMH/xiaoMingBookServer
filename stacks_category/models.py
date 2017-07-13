from django.db import models
import urllib.request
import json
from django.utils import timezone

from django.http import HttpResponse

from tools.networkTool import NetworkTool

# Create your models here.

class StacksCategory(models.Model):
    icon = models.TextField()
    category_name = models.TextField()
    category_title = models.TextField()

    def categorys(self):
        resObj = StacksCategory.objects.all()

        dataSet = []
        for k ,v in enumerate(resObj):
            obj = {
                'icon': v.icon,
                'category_name': v.category_name,
                'category_title': v.category_title,
            }
            dataSet.append(obj)
        objStr = NetworkTool.resSuccess(dataSet)
        return HttpResponse(objStr)
