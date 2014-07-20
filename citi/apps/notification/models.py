# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Notificationn(models.Model):
    """
    用户通知消息表

    """
    TYPE_CROWDFUNDING = 'crowdfunding'
    TYPE_QUESTION = 'question'
    TYPE_SYSTEM = 'system'
    TYPE = (
        (TYPE_CROWDFUNDING, u'众筹消息'),
        (TYPE_QUESTION, u'问答消息'),
        (TYPE_SYSTEM, u'系统消息'),
    )

    STATUS_UNREAD = 'unread'
    STATUS_READ = 'read'
    STATUS = (
        (STATUS_UNREAD, u'未读'),
        (STATUS_READ, u'已读'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    type = models.CharField(u'消息类型', choices=TYPE, max_length=30)
    content = models.TextField(u'消息内容')
    status = models.CharField(u'消息状态', choices=STATUS, default=STATUS_UNREAD, max_length=30)
    datetime = models.DateTimeField(u'消息生成时间', auto_now_add=True)