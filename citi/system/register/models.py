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
        subject = loader.render_to_string('registration_activation_email_subject.txt', c)
        # Email标题中不允许存在换行
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string('registration_activation_email.html', c)
        msg = EmailMultiAlternatives(subject, email, settings.EMAIL_FROM, [self.user.email])
        msg.attach_alternative(email, "text/html")
        msg.send()