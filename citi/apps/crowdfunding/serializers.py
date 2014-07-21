# -*- coding: utf-8 -*-

import logging

from rest_framework import serializers

from libs.api import fields
from .models import ProjectFeedback, ProjectPackage


logger = logging.getLogger(__name__)


class ProjectFeedbackSerializer(serializers.ModelSerializer):
    """
    项目回馈序列化

    """
    project = fields.CustomPrimaryKeyRelatedField()
    content = fields.CustomCharField()
    image = fields.CustomImageField(required=False)

    class Meta:
        model = ProjectFeedback
        fields = ('id', 'project', 'content', 'image')

    def validate(self, attrs):
        proj = attrs.get('project')
        view = self.context['view']
        # 防止越权修改项目ID为他人名下, 注意需要检测proj是否为空, PATCH时不需要此项
        if proj and proj.user != view.request.user:
            raise serializers.ValidationError('Permission denied when checking project id')
        return attrs


class ProjectPackageSerializer(serializers.ModelSerializer):
    """
    项目套餐序列化

    """
    project = fields.CustomPrimaryKeyRelatedField()
    name = fields.CustomCharField()
    money = fields.CustomFloatField()
    type = fields.CustomChoiceField(choices=ProjectPackage.TYPE)
    limit = fields.CustomIntegerField()

    class Meta:
        model = ProjectPackage
        fields = ('id', 'project', 'name', 'money', 'type', 'limit', 'feedback')