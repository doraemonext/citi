# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, nickname, password, is_auth=False, is_staff=False, is_superuser=False, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, is_auth=is_auth,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname, password, **extra_fields):
        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password, **extra_fields):
        return self._create_user(email, nickname, password, True, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(u'电子邮件地址', max_length=255, unique=True)
    nickname = models.CharField(u'昵称', max_length=30)
    is_auth = models.BooleanField(u'是否通过认证', default=False)
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