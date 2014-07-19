# -*- coding: utf-8 -*-

from rest_framework import serializers

from libs.api import fields
from .models import ProjectFeedback


class ProjectFeedbackSerializer(serializers.ModelSerializer):
    """
    项目回馈序列化

    """
    project = fields.CustomPrimaryKeyRelatedField()
    content = fields.CustomCharField()
    image = fields.CustomImageField()

    class Meta:
        model = ProjectFeedback
        fields = ('id', 'project', 'content', 'image')