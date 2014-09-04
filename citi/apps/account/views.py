# -*- coding: utf-8 -*-

import logging
import json

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.sites.models import RequestSite
from django.views.generic.base import TemplateView
from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

from apps.image.models import Image
from apps.fund.models import Order, Trade
from system.settings.models import Settings
from libs.utils.decorators import anonymous_required
from libs.api.utils import process_errors
from .forms import RegistrationForm, LoginForm, PasswordResetForm, SetPasswordForm
from .models import CustomRegistrationProfile, DetailInfo, FundInfo, BalanceInfo, ProjectInfo, QuestionInfo


logger = logging.getLogger(__name__)


class AjaxableResponseMixin(object):
    def get_form_kwargs(self):
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            dict_ = self.request.POST.copy()
            del dict_['csrfmiddlewaretoken']
            kwargs.update({
                'data': dict_,
                'files': self.request.FILES,
            })
        return kwargs

    def render_to_json_response(self, context, **response_kwargs):
        for item in context:
            context[item] = context[item][0]
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)

        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, request, form):
        if self.request.is_ajax():
            new_user = self.register(request, **form.cleaned_data)
            data = {
                'redirect_url': [reverse(self.get_success_url())],
            }
            return self.render_to_json_response(data, status=200)
        else:
            response = super(AjaxableResponseMixin, self).form_valid(request, form)
            return response


class RegistrationView(AjaxableResponseMixin, BaseRegistrationView):
    """
    注册页面相关内容

    """
    template_name = 'registration_form.html'
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        # 当用户已经登录时, 直接跳转到个人中心
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('account.profile'))

        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def register(self, request, **cleaned_data):
        """
        处理注册表单数据

        """
        email, nickname, password = cleaned_data['email'], cleaned_data['nickname'], cleaned_data['password1']
        site = RequestSite(request)
        new_user = CustomRegistrationProfile.objects.create_inactive_user(email, nickname, password, site)

        logger.info('Start the user %(user)s registration' % {'user': new_user.email})

        # 建立用户的详细信息
        detail_info = DetailInfo.objects.get(user=new_user)
        detail_info.name = cleaned_data.get('name', None)
        detail_info.sex = cleaned_data.get('sex', 'u')  # 默认为性别保密
        detail_info.age = cleaned_data.get('age', None)
        detail_info.native = cleaned_data.get('native', None)
        detail_info.profession = cleaned_data.get('profession', None)
        detail_info.idcard = cleaned_data.get('idcard', None)
        detail_info.idcard_image = cleaned_data.get('idcard_image', None)
        detail_info.mobile = cleaned_data.get('mobile', None)
        detail_info.save()

        logger.info('The user %(user)s has successfully registered. ' % {'user': new_user.email})

        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
        return new_user

    def get_success_url(self, request=None, user=None):
        """
        返回注册成功页面的name名称

        """
        return 'registration_complete'


class ActivationView(TemplateView):
    """
    激活页面显示

    """
    http_method_names = ['get']
    template_name = 'registration_activation.html'

    def __init__(self):
        self.is_activate = False
        super(ActivationView, self).__init__()

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            self.is_activate = True
        else:
            self.is_activate = False
        return super(ActivationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActivationView, self).get_context_data(**kwargs)
        context['is_activate'] = self.is_activate
        return context

    def activate(self, request, activation_key):
        activated_user = CustomRegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            logger.info('The user %(user)s has successfully activated. activation code = %(code)s', {
                'user': activated_user.email,
                'code': activation_key,
            })

            try:
                group = Group.objects.get(name=u'nocertification')
                group.user_set.add(activated_user)
            except ObjectDoesNotExist:
                logger.error(u'The group "nocertification" is not exist. The user %(user)s is not added to any group. '
                             u'You may not execute "./manage.py create_group" '
                             u'after syncdb.' % {'user': activated_user.email})

            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
        return activated_user


@anonymous_required
def login(request, template_name='login.html', authentication_form=LoginForm):
    """
    显示登陆页面并处理登陆请求, 当用户已经登陆时, 直接跳转到next所指向的页面

    """
    redirect_to = request.REQUEST.get('next', '')
    # 确保重定向链接安全, 无next参数时跳转到用户中心
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = reverse('account.profile')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            if request.is_ajax():
                return HttpResponse(json.dumps({"redirect_url": redirect_to}), status=200, content_type='application/json')
            else:
                # 用户登陆
                auth_login(request, form.get_user())
                logger.info('The user %(user)s has successfully signed in', {'user': form.get_user().email})
                return HttpResponseRedirect(redirect_to)
        else:
            if request.is_ajax():
                context = form.errors
                for item in context:
                    context[item] = context[item][0]
                return HttpResponse(json.dumps(context), status=400, content_type='application/json')
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect_to)
        form = authentication_form(request)

    context = {
        'form': form,
        'next': redirect_to,
    }
    return TemplateResponse(request, template_name, context)


def logout(request, template_name='logout.html'):
    """
    显示登出页面, 当存在跳转链接时直接登出并跳转

    """
    if request.user.is_authenticated():
        email = request.user.email
        auth_logout(request)
        logger.info('The user %(user)s has successfully signed out', {'user': email})

    redirect_to = None
    if 'next' in request.REQUEST:
        redirect_to = request.REQUEST['next']
        # 确保重定向链接安全, 否则直接删除所有GET参数并刷新logout页面
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = request.path

    if redirect_to:
        # 如果存在跳转链接, 直接进行跳转
        return HttpResponseRedirect(redirect_to)
    else:
        # 显示登出页面，提示登出成功
        context = {}
        return TemplateResponse(request, template_name, context)


@anonymous_required
@csrf_protect
def password_reset(request, template_name='password_reset_form.html',
                   email_template_name='email/password_reset_email.html',
                   subject_template_name='email/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   from_email=settings.EMAIL_FROM):
    """
    显示密码重置页面, 当提交后显示重置链接发送完成

    """
    post_reset_redirect = reverse('password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
            }
            logger.info('The password reset email of the user %(user)s starts sending.', {'user': form.get_user().email})
            form.save(request=request, **opts)
            logger.info('The password reset email of the user %(user)s has been sent.', {'user': form.get_user().email})
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    return TemplateResponse(request, template_name, context)


@anonymous_required
def password_reset_done(request, template_name='password_reset_done.html'):
    """
    显示密码重置链接发送完成页面

    """
    context = {}
    return TemplateResponse(request, template_name, context)


@anonymous_required
def password_reset_confirm(request, template_name='password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None):
    """
    密码重置确认，输入新的密码并提交

    """
    uidb64 = request.GET.get('uid', None)
    token = request.GET.get('token', None)

    user_model = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                logger.info('The process of password reset of user %(user)s has been done.', {'user': user.email})
                return HttpResponseRedirect(post_reset_redirect)
        else:
            logger.info('The password reset link of user %(user)s is clicked.', {'user': user.email})
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    return TemplateResponse(request, template_name, context)


@anonymous_required
def password_reset_complete(request, template_name='password_reset_complete.html'):
    """
    密码重置完成页面

    """
    context = {}
    return TemplateResponse(request, template_name, context)


class ProfileView(TemplateView):
    """
    个人中心页面显示

    """
    http_method_names = ['get']
    template_name = 'profile/home.jinja'

    def __init__(self):
        super(ProfileView, self).__init__()

    def get(self, request, *args, **kwargs):
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['config'] = Settings.manager.get_setting_dict()
        trades = Trade.manager.get_user_trade(user=self.request.user)
        for trade in trades:
            trade.order_info = Order.objects.get(pk=trade.order_id)
        context['trades'] = trades
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)
