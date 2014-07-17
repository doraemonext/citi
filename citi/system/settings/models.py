# -*- coding: utf-8 -*-

from django.db import models


class Settings(models.Model):
    name = models.CharField(u'设置名称', max_length=30)
    value = models.TextField(u'设置内容')