# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'rkey', 'user', 'created')
    fieldsets = (
        (None, {
            'fields': ('user', 'created')
        }),
    )
    ordering = ('-created',)


admin.site.register(Token, TokenAdmin)
