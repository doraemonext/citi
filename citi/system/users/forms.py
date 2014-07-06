# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """
    登陆表单

    """
    email = forms.EmailField(label=u'电子邮件', max_length=255, widget=forms.TextInput)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label=u'验证码')

    error_messages = {
        'invalid_login': u'您输入的用户名或密码不正确',
        'inactive': u'您的账户已被禁用',
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class PasswordResetForm(forms.Form):
    """
    密码重置表单

    """
    email = forms.EmailField(label=u'电子邮件', max_length=255)

    error_messages = {
        'invalid_email': u'您输入的邮箱不存在',
    }

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            self.user_cache = get_user_model().objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
            )

        return email

    def save(self, request, subject_template_name='password_reset_subject.txt',
             email_template_name='password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=settings.EMAIL_FROM):
        """
        表单保存时对该用户发送密码重置邮件

        """
        from django.core.mail import send_mail

        uid = urlsafe_base64_encode(force_bytes(self.user_cache.pk))
        token = token_generator.make_token(self.user_cache)
        protocol = 'https' if use_https else 'http'
        c = {
            'email': self.user_cache.email,
            'uid': uid,
            'user': self.user_cache,
            'token': token,
            'protocol': protocol,
            'url': protocol + '://' + request.get_host() + reverse('password_reset_confirm') + '?uid=' + uid + '&token=' + token,
        }
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        msg = EmailMultiAlternatives(subject, email, from_email, [self.user_cache.email])
        msg.attach_alternative(email, "text/html")
        msg.send()


class SetPasswordForm(forms.Form):
    """
    直接设置密码表单

    """
    new_password1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=u'确认新密码', widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': u'两次密码输入不匹配',
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user