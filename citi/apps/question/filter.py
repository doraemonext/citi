# -*- coding: utf-8 -*-

import django_filters

from .models import Question


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['title']