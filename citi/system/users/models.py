# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, nickname, password, is_staff=False, is_superuser=False, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password, **extra_fields):
        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password, **extra_fields):
        return self._create_user(email, nickname, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(u'电子邮件地址', max_length=255, unique=True)
    nickname = models.CharField(u'昵称', max_length=30)
    is_active = models.BooleanField(u'是否激活', default=False)
    is_staff = models.BooleanField(u'是否为管理员', default=False)
    date_joined = models.DateTimeField(u'注册日期', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'
        permissions = (
            ('view_customuser', u'Can view 用户'),
        )

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email


class DetailInfo(models.Model):
    """
    用户扩展信息表

    """
    SEX = (
        ('m', u'男'),
        ('l', u'女'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    avatar = models.ImageField(u'头像路径', upload_to='avatars', null=True, blank=True)
    name = models.CharField(u'姓名', max_length=20, null=True, blank=True)
    sex = models.CharField(u'性别', choices=SEX, max_length=1, null=True, blank=True)
    age = models.IntegerField(u'年龄', null=True, blank=True)
    idcard = models.CharField(u'身份证号', max_length=20, null=True, blank=True)
    mobile = models.CharField(u'手机号', max_length=15, null=True, blank=True)
    qq = models.CharField(u'QQ号', max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = u'用户扩展信息表'
        verbose_name_plural = u'用户扩展信息表'
        permissions = (
            ('view_detailinfo', u'Can view 用户扩展信息'),
        )


class FundInfo(models.Model):
    """
    用户资金信息表

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    alipay = models.CharField(u'支付宝账号', max_length=100, null=True, blank=True)
    bank_name = models.CharField(u'开户行名称', max_length=50, null=True, blank=True)
    bank_sub_name = models.CharField(u'支行名称', max_length=50, null=True, blank=True)
    name = models.CharField(u'开户姓名', max_length=20, null=True, blank=True)
    account = models.CharField(u'开户账号', max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = u'用户资金信息表'
        verbose_name_plural = u'用户资金信息表'
        permissions = (
            ('view_fundinfo', u'Can view 用户资金信息'),
        )


class BalanceInfo(models.Model):
    """
    用户账户余额表

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    balance = models.FloatField(u'当前余额')

    class Meta:
        verbose_name = u'用户账户余额表'
        verbose_name_plural = u'用户账户余额表'
        permissions = (
            ('view_balanceinfo', u'Can view 用户账户余额'),
        )


class ProjectInfo(models.Model):
    """
    用户项目信息表

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    launch = models.IntegerField(u'已发起项目数目', default=0)
    attention = models.IntegerField(u'已关注项目数目', default=0)
    support = models.IntegerField(u'已支持项目数目', default=0)

    class Meta:
        verbose_name = u'用户项目信息表'
        verbose_name_plural = u'用户项目信息表'
        permissions = (
            ('view_projectinfo', u'Can view 用户项目信息'),
        )


class QuestionInfo(models.Model):
    """
    用户问答信息表

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    ask = models.IntegerField(u'我提问的数目', default=0)
    answer = models.IntegerField(u'我回答的数目', default=0)
    comment = models.IntegerField(u'我评论的数目', default=0)
    vote = models.IntegerField(u'我点赞的数目', default=0)

    class Meta:
        verbose_name = u'用户问答信息表'
        verbose_name_plural = u'用户问答信息表'
        permissions = (
            ('view_questioninfo', u'Can view 用户问答信息'),
        )