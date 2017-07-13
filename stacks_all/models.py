from django.db import models
import urllib.request
import json
from django.utils import timezone

from django.http import HttpResponse

from tools.networkTool import NetworkTool


# Create your models here.

class Stacks(models.Model):
    title = models.TextField()
    imgUrl = models.TextField()
    source = models.TextField()
    author = models.TextField()
    introduce = models.TextField()
    type = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)

    # 爬虫抓取数据，存入数据库
    def creatStacks(request, param):
        url = "http://www.quanshuwang.com/list/1_" + param + ".html"
        webPage = urllib.request.urlopen(url)
        data = webPage.read()
        data = data.decode('GBK')
        data = data[data.index('<section'):data.index('</section>')]
        data = data[data.index('<ul'):data.index('</ul>')]
        result = handle(data)
        return HttpResponse(result)

    def stacksAll(request, param):
        index = 0
        if (param == ''):
            index = 0
        else:
            index = int(param)* 10
        resObj = Stacks.objects.all()[index:index + 10]
        dataSet = []
        for v, k in enumerate(resObj):
            dataObj = {
                'title': k.title,
                'imgUrl': k.imgUrl,
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
        if (lastIndex > 0):
            list.append(data[preIndex:lastIndex])
        preIndex = lastIndex
        lastIndex += 1
    for i, el in enumerate(list):
        listItem = el
        imgUrl = listItem[listItem.find('src="') + 5:listItem.find('"', listItem.find('src="') + 5)]
        title = listItem[listItem.find('title="') + 7:listItem.find('"', listItem.find('title="') + 7)]
        source = listItem[listItem.find('href="') + 6:listItem.find('"', listItem.find('href="') + 6)]
        authorIndex = listItem.find('.php?author=')
        authorIndex = listItem.find('">', authorIndex)
        authorIndex1 = listItem.find('</a>', authorIndex)
        author = listItem[authorIndex + 2:authorIndex1]
        introduceIndex = listItem.find('<em')
        introduceIndex = listItem.find('">',introduceIndex)
        introduceIndex1 = listItem.find('<a',introduceIndex)
        introduce = listItem[introduceIndex + 2:introduceIndex1]

        # imgName = imgUrl[imgUrl.rfind("/") + 1:]
        # save_file('/Users/renminghe/Desktop/python爬虫/images/', imgName, get_file(imgUrl))
        Stacks.objects.create(title=title, imgUrl=imgUrl, source=source, author=author, introduce=introduce, type="玄幻")
    return data
