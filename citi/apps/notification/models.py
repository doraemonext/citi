# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class NotificationManager(models.Manager):
    def send(self, user, type, content):
        """
        发送一条新通知消息

        """
        return super(NotificationManager, self).create(user=user, type=type, content=content,
                                                       status=Notificationn.STATUS_UNREAD)

    def read(self, pk):
        """
        将一条通知消息置为已读

        """
        notification = super(NotificationManager, self).get_queryset().get(pk=pk)
        notification.status = Notificationn.STATUS_READ
        notification.save()

    def unread(self, pk):
        """
        将一条通知消息置为未读

        """
        notification = super(NotificationManager, self).get_queryset().get(pk=pk)
        notification.status = Notificationn.STATUS_UNREAD
        notification.save()

    def delete(self, pk):
        """
        删除一条通知消息

        """
        notification = super(NotificationManager, self).get(pk=pk)
        notification.delete()

    def get(self, user=None, type=None, status=None):
        """
        获取通知消息

        """
        notification = super(NotificationManager, self).get_queryset()
        if user:
            notification = notification.filter(user=user)
        if type:
            notification = notification.filter(type=type)
        if status:
            notification = notification.filter(status=status)
        return notification


class Notificationn(models.Model):
    """
    用户通知消息表

    """
    TYPE_CROWDFUNDING = 0
    TYPE_QUESTION = 1
    TYPE_SYSTEM = 2
    TYPE = (
        (TYPE_CROWDFUNDING, u'众筹消息'),
        (TYPE_QUESTION, u'问答消息'),
        (TYPE_SYSTEM, u'系统消息'),
    )

    STATUS_UNREAD = 0
    STATUS_READ = 1
    STATUS = (
        (STATUS_UNREAD, u'未读'),
        (STATUS_READ, u'已读'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    type = models.IntegerField(u'消息类型', choices=TYPE)
    content = models.TextField(u'消息内容')
    status = models.IntegerField(u'消息状态', choices=STATUS, default=STATUS_UNREAD)
    datetime = models.DateTimeField(u'消息生成时间', auto_now_add=True)

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u'用户通知消息'
        verbose_name_plural = u'用户通知消息'
        permissions = (
            ('view_notification', 'Can view 用户通知消息'),
        )

    objects = models.Manager()
    manager = NotificationManager()