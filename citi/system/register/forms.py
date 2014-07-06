# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django import forms
from captcha.fields import CaptchaField


class RegistrationForm(forms.Form):
    """
    注册页面表单

    """
    required_css_class = 'required'

    email = forms.EmailField(label=u'电子邮件')
    nickname = forms.CharField(label=u'昵称')
    password1 = forms.CharField(widget=forms.PasswordInput, label=u'密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label=u'确认密码')
    captcha = CaptchaField(label=u'验证码')

    error_messages = {
        'exist_email': u'电子邮件已被注册',
        'password_mismatch': u'两次密码输入不匹配',
    }

    def clean_email(self):
        """
        验证电子邮件是否被使用

        """
        existing = get_user_model().objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(
                self.error_messages['exist_email'],
                code='exist_email',
            )
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        验证两次密码输入是否相等

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return self.cleaned_data