# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, logout as auth_logout

from .forms import LoginForm


@csrf_protect
@never_cache
def login(request, template_name='login.html', authentication_form=LoginForm):
    """
    显示登陆页面并处理登陆请求, 当用户已经登陆时, 直接跳转到next所指向的页面

    """
    redirect_to = request.REQUEST.get('next', '')
    # 确保重定向链接安全, 无next参数时跳转到用户中心
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # 用户登陆
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        if request.user.is_authenticated() and request.user.is_active:
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
    auth_logout(request)

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