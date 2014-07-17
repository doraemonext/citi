# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from .models import Project, ProjectCover, ProjectCategory


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'now_money', 'status', 'attention_count', 'post_datetime', 'modify_datetime']

