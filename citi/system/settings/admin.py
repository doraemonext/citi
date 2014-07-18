# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Settings


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('description', 'value')
    ordering = ('id', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Settings, SettingsAdmin)
