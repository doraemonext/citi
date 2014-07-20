# -*- coding: utf-8 -*-

import hashlib
import random

from django.db import models
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings
from registration.models import RegistrationManager, RegistrationProfile
from mptt.models import TreeForeignKey

from apps.location.models import Location


class CustomRegistrationManager(RegistrationManager):
    """
    继承自RegistrationManager, 自定义用户字段

    """
    def create_inactive_user(self, email, nickname, password, site, send_email=True):
        """
        新建一个未激活的用户

        """
        new_user = get_user_model().objects.create_user(email, nickname, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)
        registration_profile.send_activation_email(site)

        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        """
        通过用户的电子邮件地址创建一个唯一的和用户绑定的激活码

        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        email = user.email
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        activation_key = hashlib.sha1(salt+email).hexdigest()
        return self.create(user=user, activation_key=activation_key)


class CustomRegistrationProfile(RegistrationProfile):
    """
    继承自RegistrationProfile, 自定义模板路径及邮件发送问题

    """
    objects = CustomRegistrationManager()

    class Meta:
        verbose_name = u'注册激活码'
        verbose_name_plural = u'注册激活码'
        proxy = True

    def send_activation_email(self, site):
        c = {
            'activation_key': self.activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
        }
        subject = loader.render_to_string('email/registration_activation_email_subject.txt', c)
        # Email标题中不允许存在换行
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string('email/registration_activation_email.html', c)
        msg = EmailMultiAlternatives(subject, email, settings.EMAIL_FROM, [self.user.email])
        msg.attach_alternative(email, "text/html")
        msg.send()


class DetailInfo(models.Model):
    """
    用户扩展信息表

    """
    SEX = (
        ('u', u'保密'),
        ('m', u'男'),
        ('l', u'女'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    avatar = models.ImageField(u'头像路径', upload_to='avatars', null=True, blank=True)
    name = models.CharField(u'姓名', max_length=20, null=True, blank=True)
    sex = models.CharField(u'性别', choices=SEX, max_length=1, null=True, blank=True)
    age = models.IntegerField(u'年龄', null=True, blank=True)
    native = TreeForeignKey(Location, verbose_name=u'籍贯', null=True, blank=True)
    profession = models.CharField(u'职业', max_length=100, null=True, blank=True)
    idcard = models.CharField(u'身份证号', max_length=20, null=True, blank=True)
    idcard_image = models.ImageField(u'身份证照片', upload_to='idcard', null=True, blank=True)
    mobile = models.CharField(u'手机号', max_length=15, null=True, blank=True)
    qq = models.CharField(u'QQ号', max_length=15, null=True, blank=True)
    weibo = models.CharField(u'微博', max_length=50, null=True, blank=True)
    blog = models.CharField(u'博客', max_length=50, null=True, blank=True)

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
    balance = models.FloatField(u'当前余额', default=0.0)

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
