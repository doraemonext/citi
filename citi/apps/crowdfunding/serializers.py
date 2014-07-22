# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.image.models import Image
from libs.api import fields
from .models import ProjectFeedback, ProjectPackage


logger = logging.getLogger(__name__)


class ProjectFeedbackSerializer(serializers.ModelSerializer):
    """
    项目回馈序列化

    """
    project = fields.CustomPrimaryKeyRelatedField()
    content = fields.CustomCharField()
    image = fields.CustomIntegerField(required=False)

    class Meta:
        model = ProjectFeedback
        fields = ('id', 'project', 'content', 'image')

    def validate_image(self, attrs, source):
        if source in attrs:
            data = attrs[source]
            try:
                image = Image.objects.get(pk=data)
            except ObjectDoesNotExist:
                raise serializers.ValidationError('Invalid image ID')
            if image.type != Image.TYPE_FEEDBACK:
                raise serializers.ValidationError('Invalid image type')
            if not image.user:
                raise serializers.ValidationError('Invalid image user (no user)')
            if self.context['view'].request.user != image.user:
                raise serializers.ValidationError('Invalid image user (other user)')

        return attrs

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

    def validate_feedback(self, attrs, source):
        data = attrs[source]
        if not data:
            raise serializers.ValidationError('Required data')
        return attrs

    def validate(self, attrs):
        proj = attrs.get('project')
        view = self.context['view']
        # 防止越权修改项目ID为他人名下, 注意需要检测proj是否为空, PATCH时不需要此项
        if proj and proj.user != view.request.user:
            raise serializers.ValidationError('Permission denied when checking project id')
        return attrs