from django.db import models
import urllib.request
import json
import re
from django.utils import timezone

from django.http import HttpResponse

from tools.networkTool import NetworkTool


# Create your models here.

class Stacks(models.Model):
    title = models.TextField()
    source = models.TextField()
    author = models.TextField()
    introduce = models.TextField()
    type = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)

    # 爬虫抓取数据，存入数据库
    def creatStacks(request, param):
        url = "http://book.zongheng.com/store/c" + param + "/c0/b0/u0/p1/v0/s9/t0/ALL.html"
        webPage = urllib.request.urlopen(url)
        data = webPage.read()
        data = data.decode('utf-8')
        data = data[data.index('<ul class="main_con">') + len('<ul class="main_con">'):data.index('<div class="page">')]
        data = data[:data.index('</ul>')]
        result = handle(data)
        return HttpResponse(result)

    def stacksAll(request, param1, param2):
        index = 0
        typeMap = {
            "1" : "奇幻玄幻",
        }
        if (param2 == ''):
            index = 0
        else:
            index = int(param2)* 10

        resObj = Stacks.objects.filter(type = typeMap[param1])[index:index + 10]
        dataSet = []
        for v, k in enumerate(resObj):
            dataObj = {
                'title': k.title,
                'source': k.source,
                'author': k.author,
                'introduce': k.introduce,
                'type': k.type,
            }
            dataSet.append(dataObj)
        resJson = NetworkTool.resSuccess(dataSet)
        return HttpResponse(resJson)


'''
抓取网页文件内容，保存到内存

@url 欲抓取文件 ，path+filename
'''


def get_file(url):
    try:

        req = urllib.request.urlopen(url)
        data = req.read()
        return data
    except BaseException as e:
        print(e)
        return None


'''
保存文件到本地

@path  本地路径
@file_name 文件名
@data 文件内容
'''


def save_file(path, file_name, data):
    if data == None:
        return

    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


def handle(data):
    lastIndex = 0
    preIndex = 0
    list = []
    dataLen = data.rfind('</li>')
    while lastIndex < dataLen:
        lastIndex = data.find('</li>', lastIndex, len(data))
        if (lastIndex > 0 and data[preIndex:lastIndex].find('<li class="line') < 0):
            list.append(data[preIndex:lastIndex])
        preIndex = lastIndex
        lastIndex += 1
    for i, el in enumerate(list):
        listItem = el
        title = listItem[listItem.find('<span class="chap">') + len('<span class="chap">'):listItem.find(
            '<span class="number">')]
        title = title[title.find('">') + len('">'):title.find('</a>')]

        source = listItem[listItem.find('<span class="chap">') + len('<span class="chap">'):listItem.find(
            '<span class="number">')]
        source = source[source.find('href="') + len('href="'):source.find('" title="')]

        author = listItem[listItem.find('<span class="author">') + len('<span class="author">'):listItem.find(
            '<span class="time">')]
        author = author[author.find('">') + len('">'):author.find('</a>')]

        introduce = listItem[listItem.find('<span class="number">') + len('<span class="number">'):listItem.find(
            '<span class="author">')]
        introduce = re.search(r'\d+', introduce).group()

        # imgName = imgUrl[imgUrl.rfind("/") + 1:]
        # save_file('/Users/renminghe/Desktop/python爬虫/images/', imgName, get_file(imgUrl))
        Stacks.objects.create(title=title, source=source, author=author, introduce=introduce, type="奇幻玄幻")
    return data
