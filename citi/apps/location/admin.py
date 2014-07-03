# -*- coding: utf-8 -*-

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Location


class LocationAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Location, LocationAdmin)