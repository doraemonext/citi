# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from awesome_avatar.fields import AvatarField

# For South Migration
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^awesome_avatar\.fields\.AvatarField"])


class Detail(models.Model):
    """
    用户扩展信息表

    """
    SEX = (
        ('m', 'Male'),
        ('l', 'Lady'),
    )

    user = models.OneToOneField(User, verbose_name=u'所属用户')
    avatar = models.ImageField(u'头像路径', upload_to='avatars', null=True, blank=True)
    name = models.CharField(u'姓名', max_length=20, null=True, blank=True)
    sex = models.CharField(u'性别', choices=SEX, max_length=1, null=True, blank=True)
    age = models.IntegerField(u'年龄', null=True, blank=True)
    idcard = models.CharField(u'身份证号', max_length=20, null=True, blank=True)
    mobile = models.CharField(u'手机号', max_length=15, null=True, blank=True)
    qq = models.CharField(u'QQ号', max_length=15, null=True, blank=True)


class FundInfo(models.Model):
    """
    用户资金信息表

    """
    user = models.OneToOneField(User, verbose_name=u'所属用户')
    alipay = models.CharField(u'支付宝账号', max_length=100, null=True, blank=True)
    bank_name = models.CharField(u'开户行名称', max_length=50, null=True, blank=True)
    bank_sub_name = models.CharField(u'支行名称', max_length=50, null=True, blank=True)
    name = models.CharField(u'开户姓名', max_length=20, null=True, blank=True)
    account = models.CharField(u'开户账号', max_length=30, null=True, blank=True)


class Balance(models.Model):
    """
    用户账户余额表

    """
    user = models.OneToOneField(User, verbose_name=u'所属用户')
    balance = models.FloatField(u'当前余额')


class Project(models.Model):
    """
    用户项目信息表

    """
    user = models.OneToOneField(User, verbose_name=u'所属用户')
    launch = models.IntegerField(u'已发起项目数目', default=0)
    attention = models.IntegerField(u'已关注项目数目', default=0)
    support = models.IntegerField(u'已支持项目数目', default=0)


class Question(models.Model):
    """
    用户问答信息表

    """
    user = models.OneToOneField(User, verbose_name=u'所属用户')
    ask = models.IntegerField(u'我提问的数目', default=0)
    answer = models.IntegerField(u'我回答的数目', default=0)
    comment = models.IntegerField(u'我评论的数目', default=0)
    vote = models.IntegerField(u'我点赞的数目', default=0)