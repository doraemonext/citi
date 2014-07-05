# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
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