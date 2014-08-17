# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.image.models import Image
from libs.api import fields
from .models import ProjectCategory, Project, ProjectFeedback, ProjectPackage, ProjectComment, ProjectSupport, ProjectTopic, ProjectTopicComment


logger = logging.getLogger(__name__)


class ProjectCategorySerializer(serializers.ModelSerializer):
    """
    地理位置序列化

    """
    class Meta:
        model = ProjectCategory
        fields = ('id', 'name')


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目序列化

    """
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    name = fields.CustomCharField()
    cover = fields.CustomIntegerField()
    location = fields.CustomPrimaryKeyRelatedField()
    location_detail = fields.CustomCharField(required=False)
    category = fields.CustomPrimaryKeyRelatedField()
    total_money = fields.CustomFloatField()
    total_days = fields.CustomIntegerField()
    summary = fields.CustomCharField()
    content = fields.CustomCharField()
    now_money = fields.CustomFloatField(read_only=True)
    status = fields.CustomChoiceField(read_only=True)
    attention_count = fields.CustomIntegerField(read_only=True)
    tags = fields.CustomTagField(required=False)
    post_datetime = fields.CustomDateTimeField(read_only=True)
    modify_datetime = fields.CustomDateTimeField(read_only=True)
    feedback = SerializerMethodField('get_feedback')
    package = SerializerMethodField('get_package')

    class Meta:
        model = Project
        fields = (
            'id', 'user', 'name', 'cover', 'location', 'location_detail', 'category',
            'total_money', 'total_days', 'summary', 'content', 'now_money', 'status',
            'attention_count', 'tags', 'post_datetime', 'modify_datetime',
            'feedback', 'package',
        )

    def get_feedback(self, obj):
        feedback = ProjectFeedback.objects.filter(project=obj)
        return [item.pk for item in feedback]

    def get_package(self, obj):
        package = ProjectPackage.objects.filter(project=obj)
        return [item.pk for item in package]

    def validate_cover(self, attrs, source):
        if source in attrs:
            data = attrs[source]
            try:
                image = Image.objects.get(pk=data)
            except ObjectDoesNotExist:
                raise serializers.ValidationError('Invalid image ID')
            if image.type != Image.TYPE_COVER:
                raise serializers.ValidationError('Invalid image type')
            if not image.user:
                raise serializers.ValidationError('Invalid image user (no user)')
            if self.context['view'].request.user != image.user:
                raise serializers.ValidationError('Invalid image user (other user)')

        return attrs

    def save_object(self, obj, **kwargs):
        # 修正location_detail在PUT下不能更新的问题
        view = self.context['view']
        if view.request.method == 'PUT' and not view.request.DATA.get('location_detail', None):
            obj.location_detail = None

        super(ProjectSerializer, self).save_object(obj, **kwargs)


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


class ProjectCommentSerializer(serializers.ModelSerializer):
    """
    项目评论序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    email = fields.CustomCharField(source='get_user_email', required=False)
    content = fields.CustomCharField()
    datetime = fields.CustomDateTimeField(read_only=True)
    parent = fields.CustomPrimaryKeyRelatedField(required=False)
    children = fields.CustomRecursiveField(many=True, read_only=True)
    type = fields.CustomCharField(write_only=True)

    class Meta:
        model = ProjectComment
        fields = ('id', 'project', 'user', 'email', 'content', 'datetime', 'parent', 'children', 'type')

    def validate_type(self, attrs, source):
        data = attrs[source]
        if self.context['view'].request.user.is_authenticated():
            if data == 'anonymous' or data == 'normal':
                return attrs
        else:
            if data == 'anonymous':
                return attrs
            elif data == 'normal':
                raise serializers.ValidationError('Error comment type, you are not authenticated')

        raise serializers.ValidationError('Invalid data')

    def restore_object(self, attrs, instance=None):
        obj = super(ProjectCommentSerializer, self).restore_object(attrs, instance)
        type = attrs.pop('type', None)
        if type == 'anonymous':
            obj.user = None
        else:
            obj.user = self.context['view'].request.user
        return obj


class ProjectSupportSerializer(serializers.ModelSerializer):
    """
    项目支持序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    package = fields.CustomPrimaryKeyRelatedField(read_only=True)
    money = fields.CustomFloatField(read_only=True)
    status = fields.CustomIntegerField(read_only=True)
    datetime = fields.CustomDateTimeField(read_only=True)

    class Meta:
        model = ProjectSupport
        fields = ('id', 'project', 'user', 'package', 'money', 'status', 'datetime')


class ProjectTopicSerializer(serializers.ModelSerializer):
    """
    项目主题序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    title = fields.CustomCharField()
    content = fields.CustomCharField()
    post_datetime = fields.CustomDateTimeField(read_only=True)
    modify_datetime = fields.CustomDateTimeField(read_only=True)

    class Meta:
        model = ProjectTopic
        fields = ('id', 'project', 'user', 'title', 'content', 'post_datetime', 'modify_datetime')


class ProjectTopicCommentSerializer(serializers.ModelSerializer):
    """
    项目主题评论序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    topic = fields.CustomPrimaryKeyRelatedField(read_only=True)
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    content = fields.CustomCharField()
    datetime = fields.CustomDateTimeField(read_only=True)
    parent = fields.CustomPrimaryKeyRelatedField()
    children = fields.CustomRecursiveField(many=True, read_only=True)

    class Meta:
        model = ProjectTopicComment
        fields = ('id', 'project', 'topic', 'user', 'content', 'datetime', 'parent', 'children')