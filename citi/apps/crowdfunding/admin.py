# -*- coding: utf-8 -*-

from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import ProjectCategory


class ProjectCategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 40
    list_display = ('name', )

    sortable = 'order'

admin.site.register(ProjectCategory, ProjectCategoryAdmin)