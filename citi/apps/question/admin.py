# -*- coding: utf-8 -*-

from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Question, QuestionAnswer


class QuestionAdmin(admin.ModelAdmin):
    pass

class QuestionAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)