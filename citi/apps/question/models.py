# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    问题表

    """
    user = models.ForeignKey(User, verbose_name=u'所属用户')
    title = models.CharField(u'问题名称', max_length=255)
    content = models.TextField(u'问题内容')
    answer_count = models.IntegerField(u'回答数目', default=0)
    comment_count = models.IntegerField(u'评论数目', default=0)
    post_datetime = models.DateTimeField(u'发布日期', auto_now_add=True)
    modify_datetime = models.DateTimeField(u'最后修改日期', auto_now=True)


class QuestionAnswer(models.Model):
    """
    问题回答表

    """
    question = models.ForeignKey(Question, verbose_name=u'所属问题')
    user = models.ForeignKey(User, verbose_name=u'所属用户')
    content = models.TextField(u'回答内容')
    vote_count = models.IntegerField(u'点赞数目', default=0)
    comment_count = models.IntegerField(u'评论数目', default=0)
    post_datetime = models.DateTimeField(u'发布日期', auto_now_add=True)
    modify_datetime = models.DateTimeField(u'最后修改日期', auto_now=True)


    