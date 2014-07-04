# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Detail, FundInfo, Balance, Project, Question


class DetailInline(admin.StackedInline):
    model = Detail
    can_delete = False
    verbose_name = u'用户扩展信息'
    verbose_name_plural = u'用户扩展信息'


class FundInfoInline(admin.StackedInline):
    model = FundInfo
    can_delete = False
    verbose_name = u'用户资金信息表'
    verbose_name_plural = u'用户资金信息表'


class BalanceInline(admin.StackedInline):
    model = Balance
    can_delete = False
    verbose_name = u'用户账户余额表'
    verbose_name_plural = u'用户账户余额表'


class ProjectInline(admin.StackedInline):
    model = Project
    can_delete = False
    verbose_name = u'用户项目信息表'
    verbose_name_plural = u'用户项目信息表'


class QuestionInline(admin.StackedInline):
    model = Question
    can_delete = False
    verbose_name = u'用户回答信息表'
    verbose_name_plural = u'用户回答信息表'


class UserAdmin(UserAdmin):
    inlines = (DetailInline, FundInfoInline, BalanceInline, ProjectInline, QuestionInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)