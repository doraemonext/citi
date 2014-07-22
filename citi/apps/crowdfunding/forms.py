# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

from apps.image.models import Image
from .models import Project, ProjectCategory


class ProjectForm(forms.ModelForm):
    error_messages = {
        'invalid_cover': u'您的项目封面图片非法',
    }

    class Meta:
        model = Project
        exclude = ['user', 'now_money', 'status', 'attention_count', 'post_datetime', 'modify_datetime']

    def clean_cover(self):
        data = self.cleaned_data['cover']
        try:
            Image.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_cover'],
                code='invalid_cover',
            )

        return data