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
from mptt.forms import TreeNodeChoiceField

from apps.image.models import Image
from apps.location.models import Location


class RegistrationForm(forms.Form):
    """
    注册页面表单

    """
    SEX = (
        ('u', u'保密'),
        ('m', u'男'),
        ('l', u'女'),
    )

    required_css_class = 'required'

    email = forms.EmailField(label=u'电子邮件')
    nickname = forms.CharField(label=u'昵称')
    password1 = forms.CharField(widget=forms.PasswordInput, label=u'密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label=u'确认密码')
    name = forms.CharField(label=u'姓名', required=False)
    sex = forms.ChoiceField(label=u'性别', choices=SEX, required=False)
    age = forms.IntegerField(label=u'年龄', required=False)
    native = TreeNodeChoiceField(label=u'籍贯', queryset=Location.objects.all(), empty_label='', required=False)
    profession = forms.CharField(label=u'职业', required=False)
    idcard = forms.CharField(label=u'身份证号', required=False)
    idcard_image = forms.IntegerField(label=u'身份证照片', required=False)
    mobile = forms.CharField(label=u'手机号', required=False)
    # captcha = CaptchaField(label=u'验证码')

    error_messages = {
        'exist_email': u'电子邮件已被注册',
        'password_mismatch': u'两次密码输入不匹配',
        'detail_incomplete': u'详细信息不完整',
        'idcard_image_invalid': u'身份证图片ID错误',
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

    def get_and_set_cleaned_data(self, name):
        """
        获得验证后的数据, 当数据为空时，设置该值为None并返回None

        """
        data = self.cleaned_data.get(name, None)
        if not data:
            self.cleaned_data[name] = None
            return None
        else:
            return data

    def clean(self):
        """
        对表单合法性进行最终验证

        """
        # 验证两次密码输入是否相等
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        # 如果输入详细信息中的任意一种, 则其他详细信息必须填写
        name = self.get_and_set_cleaned_data('name')
        sex = self.get_and_set_cleaned_data('sex')
        age = self.get_and_set_cleaned_data('age')
        idcard = self.get_and_set_cleaned_data('idcard')
        idcard_image = self.get_and_set_cleaned_data('idcard_image')
        mobile = self.get_and_set_cleaned_data('mobile')
        if idcard_image and not Image.objects.filter(pk=idcard_image).exists():
            raise forms.ValidationError(
                self.error_messages['idcard_image_invalid'],
                code='idcard_image_invalid',
            )
        if name or (sex == 'm' or sex == 'l') or age or idcard or idcard_image or mobile:
            if name and (sex == 'm' or sex == 'l') and age and idcard and mobile:
                pass
            else:
                raise forms.ValidationError(
                    self.error_messages['detail_incomplete'],
                    code='detail_incomplete'
                )
        return self.cleaned_data


class LoginForm(forms.Form):
    """
    登陆表单

    """
    email = forms.EmailField(label=u'电子邮件', max_length=255, widget=forms.TextInput)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    # captcha = CaptchaField(label=u'验证码')

    error_messages = {
        'invalid_login': u'您输入的用户名或密码不正确',
        'inactive': u'您的账户尚未激活, 请到邮箱中检查激活链接',
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

    def get_user(self):
        return self.user_cache

    def save(self, request, subject_template_name='email/password_reset_subject.txt',
             email_template_name='email/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=settings.EMAIL_FROM):
        """
        表单保存时对该用户发送密码重置邮件

        """
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
