# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple

from system.users.models import CustomUser
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


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'确认密码', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'两次密码输入不匹配')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('nickname', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial['password']


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'nickname', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (u'昵称', {'fields': ('nickname',)}),
        (u'是否激活', {'fields': ('is_active',)}),
        (u'管理权限', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'nickname')
    ordering = ('email', 'nickname')
    filter_horizontal = ()
    inlines = (DetailInline, FundInfoInline, BalanceInline, ProjectInline, QuestionInline)


class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Users',
            is_stacked=False
        )
    )

    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        group = super(GroupAdminForm, self).save(commit=False)

        if commit:
            group.save()

        if group.pk:
            group.user_set = self.cleaned_data['users']
            self.save_m2m()

        return group


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)