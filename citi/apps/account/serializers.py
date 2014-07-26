# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from libs.api import fields

from .models import DetailInfo, FundInfo, BalanceInfo, ProjectInfo, QuestionInfo


class DetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailInfo
        exclude = ('id', 'user')


class FundInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundInfo
        exclude = ('id', 'user')


class BalanceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceInfo
        exclude = ('id', 'user')


class ProjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInfo
        exclude = ('id', 'user')


class QuestionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionInfo
        exclude = ('id', 'user')


class UserSerializer(serializers.ModelSerializer):
    email = fields.CustomCharField()
    nickname = fields.CustomCharField()
    is_active = fields.CustomBooleanField()
    is_staff = fields.CustomBooleanField()
    is_authentication = fields.CustomBooleanField()
    date_joined = fields.CustomDateTimeField()
    detailinfo = DetailInfoSerializer()
    fundinfo = FundInfoSerializer()
    balanceinfo = BalanceInfoSerializer()
    projectinfo = ProjectInfoSerializer()
    questioninfo = QuestionInfoSerializer()

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'nickname', 'is_active', 'is_staff', 'is_authentication', 'date_joined',
            'detailinfo', 'fundinfo', 'balanceinfo', 'projectinfo', 'questioninfo',
        )
