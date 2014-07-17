# -*- coding: utf-8 -*-

from django.db import models


class Settings(models.Model):
    name = models.CharField(u'设置名称', max_length=30)
    value = models.TextField(u'设置内容')

    class Meta:
        verbose_name = u'系统设置'
        verbose_name_plural = u'系统设置'
        permissions = (
            ('view_settings', u'Can view 系统设置'),
        )