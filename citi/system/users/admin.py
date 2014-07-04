# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import DetailInfo, FundInfo, BalanceInfo, ProjectInfo, QuestionInfo


class DetailInline(admin.StackedInline):
    model = DetailInfo
    can_delete = False
    verbose_name = u'用户扩展信息'
    verbose_name_plural = u'用户扩展信息'


class FundInfoInline(admin.StackedInline):
    model = FundInfo
    can_delete = False
    verbose_name = u'用户资金信息表'
    verbose_name_plural = u'用户资金信息表'


class BalanceInline(admin.StackedInline):
    model = BalanceInfo
    can_delete = False
    verbose_name = u'用户账户余额表'
    verbose_name_plural = u'用户账户余额表'


class ProjectInline(admin.StackedInline):
    model = ProjectInfo
    can_delete = False
    verbose_name = u'用户项目信息表'
    verbose_name_plural = u'用户项目信息表'


class QuestionInline(admin.StackedInline):
    model = QuestionInfo
    can_delete = False
    verbose_name = u'用户回答信息表'
    verbose_name_plural = u'用户回答信息表'


class UserAdmin(UserAdmin):
    inlines = (DetailInline, FundInfoInline, BalanceInline, ProjectInline, QuestionInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)