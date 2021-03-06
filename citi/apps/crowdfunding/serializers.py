# -*- coding: utf-8 -*-

import logging
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.account.serializers import UserSerializer
from apps.image.models import Image
from libs.api import fields
from .models import ProjectCategory, Project, ProjectFeedback, ProjectPackage, ProjectComment, ProjectSupport, ProjectAttention, ProjectTopic, ProjectTopicComment, ProjectSection, ProjectTask


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
    remaining_days = SerializerMethodField('get_remaining_days')
    summary = fields.CustomCharField()
    content = fields.CustomCharField()
    now_money = fields.CustomFloatField(read_only=True)
    status = fields.CustomChoiceField(read_only=True)
    attention_count = fields.CustomIntegerField(read_only=True)
    support_count = SerializerMethodField('get_support_count')
    normal_support_count = SerializerMethodField('get_normal_support_count')
    partner_support_count = SerializerMethodField('get_partner_support_count')
    #tags = fields.CustomTagField(required=False)
    post_datetime = fields.CustomDateTimeField(read_only=True)
    modify_datetime = fields.CustomDateTimeField(read_only=True)
    feedback = SerializerMethodField('get_feedback')
    package = SerializerMethodField('get_package')
    personal_information = SerializerMethodField('get_personal_information')

    class Meta:
        model = Project
        fields = (
            'id', 'user', 'name', 'cover', 'location', 'location_detail', 'category',
            'total_money', 'total_days', 'remaining_days', 'summary', 'content', 'now_money', 'status',
            'attention_count', 'support_count', 'normal_support_count', 'partner_support_count', 'post_datetime', 'modify_datetime',
            'feedback', 'package', 'personal_information'
        )

    def get_feedback(self, obj):
        feedback = ProjectFeedback.objects.filter(project=obj)
        return [item.pk for item in feedback]

    def get_package(self, obj):
        package = ProjectPackage.objects.filter(project=obj)
        return [item.pk for item in package]

    def get_remaining_days(self, obj):
        datetime_end = obj.post_datetime + datetime.timedelta(days=obj.total_days)
        remaining_days = (datetime_end - timezone.now()).days
        if remaining_days > 0:
            return remaining_days
        else:
            return 0

    def get_support_count(self, obj):
        return ProjectSupport.objects.filter(project=obj).count()

    def get_normal_support_count(self, obj):
        return ProjectSupport.manager.get_normal_support(project=obj).count()

    def get_partner_support_count(self, obj):
        return ProjectSupport.manager.get_partner_support(project=obj).count()

    def get_personal_information(self, obj):
        try:
            request = self.context['request']
        except KeyError:
            return {}

        info = {}
        if request.user.is_authenticated():
            if ProjectAttention.manager.is_attention(project=obj, user=request.user):
                info['is_attended'] = True
            else:
                info['is_attended'] = False

            if ProjectSupport.manager.has_support(project=obj, user=request.user):
                info['is_supported'] = True
            else:
                info['is_supported'] = False

            if info['is_supported']:
                info['support_type'] = ProjectSupport.objects.filter(project=obj).filter(user=request.user).first().package.type
            else:
                info['support_type'] = -1

        return info


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
    project = ProjectSerializer(read_only=True)
    package = fields.CustomPrimaryKeyRelatedField(read_only=True)
    money = fields.CustomFloatField(read_only=True)
    status = fields.CustomIntegerField(read_only=True)
    datetime = fields.CustomDateTimeField(read_only=True)

    class Meta:
        model = ProjectSupport
        fields = ('id', 'project', 'package', 'money', 'status', 'datetime')


class ProjectAttentionSerializer(serializers.ModelSerializer):
    """
    项目关注序列化

    """
    project = ProjectSerializer(read_only=True)
    datetime = fields.CustomDateTimeField(read_only=True)

    class Meta:
        model = ProjectAttention
        fields = ('id', 'project', 'datetime')


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
    parent = fields.CustomPrimaryKeyRelatedField(required=False)
    children = fields.CustomRecursiveField(many=True, read_only=True)

    class Meta:
        model = ProjectTopicComment
        fields = ('id', 'project', 'topic', 'user', 'content', 'datetime', 'parent', 'children')


class ProjectSectionSerializer(serializers.ModelSerializer):
    """
    项目阶段序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    title = fields.CustomCharField()
    description = fields.CustomCharField()
    status = fields.CustomIntegerField()
    order = fields.CustomIntegerField()

    class Meta:
        model = ProjectSection
        fields = ('id', 'project', 'title', 'description', 'status', 'order')


class ProjectTaskSerializer(serializers.ModelSerializer):
    """
    项目任务序列化

    """
    project = fields.CustomPrimaryKeyRelatedField(read_only=True)
    section = fields.CustomPrimaryKeyRelatedField()
    content = fields.CustomCharField()
    status = fields.CustomIntegerField()
    order = fields.CustomIntegerField()

    class Meta:
        model = ProjectTask
        fields = ('id', 'project', 'section', 'content', 'status', 'order')