# -*- coding: utf-8 -*-

from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Location


class LocationAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', )

    sortable = 'order'

admin.site.register(Location, LocationAdmin)