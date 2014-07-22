# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from imagekit.models import ImageSpecField


class Image(models.Model):
    TYPE_IDCARD = 0
    TYPE_AVATAR = 1
    TYPE_UNKNOWN = 99
    TYPE = (
        (TYPE_IDCARD, u'身份证照片'),
        (TYPE_AVATAR, u'用户头像'),
        (TYPE_UNKNOWN, u'未知类型'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户', blank=True, null=True)
    type = models.IntegerField(u'图片类型', choices=TYPE)
    image = models.ImageField(u'图片路径', upload_to='images')
    datetime = models.DateTimeField(u'图片上传时间', auto_now_add=True)

    def __unicode__(self):
        return self.path

    class Meta:
        verbose_name = u'图片存储'
        verbose_name_plural = u'图片存储'
        permissions = (
            ('view_image', u'Can view 图片存储'),
        )