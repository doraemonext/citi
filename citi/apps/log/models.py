# -*- coding: utf-8 -*-

from django.db import models


class Log(models.Model):
    user_id = models.IntegerField(u'操作用户ID')
    type = models.CharField(u'操作类型', max_length=30)
    content = models.TextField(u'操作内容')
    datetime = models.DateTimeField(u'操作时间', auto_now=True)
