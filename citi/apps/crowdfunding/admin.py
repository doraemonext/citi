# -*- coding: utf-8 -*-

from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import ProjectCategory, Project, ProjectFeedback, ProjectPackage, ProjectAttention, ProjectComment


class ProjectCategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 40
    list_display = ('name', )

    sortable = 'order'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'summary', 'total_days', 'total_money', 'status', 'post_datetime', 'modify_datetime')
    list_filter = ('status', )
    search_fields = ('name', 'user__email')
    ordering = ('-post_datetime', )

    def has_add_permission(self, request):
        return False


class ProjectFeedbackAdmin(admin.ModelAdmin):
    list_display = ('content', 'image', 'project')
    search_fields = ('content', 'project__name')
    ordering = ('-id', )
    exclude = ('order', )

    def has_add_permission(self, request):
        return False


class ProjectPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'money', 'type', 'limit')
    list_filter = ('type', )
    search_fields = ('name', 'project')
    ordering = ('-id', )

    def has_add_permission(self, request):
        return False


class ProjectAttentionAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'datetime')
    ordering = ('-id', )
    search_fields = ('project__name', 'user__email')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'project', 'user', 'datetime')
    ordering = ('-datetime', )
    search_fields = ('content', 'project__name', 'user__email')

    def has_add_permission(self, request):
        return False


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFeedback, ProjectFeedbackAdmin)
admin.site.register(ProjectPackage, ProjectPackageAdmin)
admin.site.register(ProjectAttention, ProjectAttentionAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)