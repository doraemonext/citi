# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from libs.api import fields

from .models import DetailInfo, FundInfo, BalanceInfo, ProjectInfo, QuestionInfo


class DetailInfoSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = DetailInfo
        exclude = ('id', 'user')


class FundInfoSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = FundInfo
        exclude = ('id', 'user')


class BalanceInfoSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = BalanceInfo
        exclude = ('id', 'user')


class ProjectInfoSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = ProjectInfo
        exclude = ('id', 'user')


class QuestionInfoSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = QuestionInfo
        exclude = ('id', 'user')


class UserSerializer(serializers.ModelSerializer):
    email = fields.CustomCharField(read_only=True)
    nickname = fields.CustomCharField()
    is_active = fields.CustomBooleanField(read_only=True)
    is_staff = fields.CustomBooleanField(read_only=True)
    is_authentication = fields.CustomBooleanField(read_only=True)
    date_joined = fields.CustomDateTimeField(read_only=True)
    detailinfo = DetailInfoSerializer(required=False)
    fundinfo = FundInfoSerializer(required=False)
    balanceinfo = BalanceInfoSerializer(read_only=True)
    projectinfo = ProjectInfoSerializer(read_only=True)
    questioninfo = QuestionInfoSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'nickname', 'is_active', 'is_staff', 'is_authentication', 'date_joined',
            'detailinfo', 'fundinfo', 'balanceinfo', 'projectinfo', 'questioninfo',
        )


class DetailInfoAnonymousSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    class Meta:
        model = DetailInfo
        fields = ('avatar', 'native', 'profession', 'qq', 'weibo', 'blog')


class UserAnonymousSerializer(serializers.ModelSerializer):
    email = fields.CustomCharField(read_only=True)
    nickname = fields.CustomCharField(read_only=True)
    detailinfo = DetailInfoAnonymousSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'nickname', 'detailinfo')