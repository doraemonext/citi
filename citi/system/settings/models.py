# -*- coding: utf-8 -*-

from django.db import models, DatabaseError


class SettingsManager(models.Manager):
    def get_setting(self, name):
        """
        获取设置

        返回该设置项的value, 为str类型
        :param name: 返回指定的设置项的value
        :return: str
        """
        result = super(SettingsManager, self).get_queryset().filter(name=name)

        if result.count() == 0:
            raise DatabaseError('Cannot find matching setting object.')
        elif result.count() > 1:
            raise DatabaseError('Multi setting objects are found.')

        return result.values()[0]['value']

    def get_setting_dict(self):
        """
        获取设置dict
        :return: dict
        """
        queryset = super(SettingsManager, self).get_queryset()
        result = {}
        for item in queryset:
            result[item.name] = item.value
        return result


class Settings(models.Model):
    name = models.CharField(u'设置名称', max_length=30, editable=False)
    description = models.CharField(u'设置描述', max_length=255, editable=False)
    value = models.TextField(u'设置内容')

    class Meta:
        verbose_name = u'系统设置'
        verbose_name_plural = u'系统设置'
        permissions = (
            ('view_settings', u'Can view 系统设置'),
        )

    def __unicode__(self):
        return self.description

    objects = models.Manager()
    manager = SettingsManager()