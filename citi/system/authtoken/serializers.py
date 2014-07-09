# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from libs.api.serializers import CustomSerializer
from system.authtoken.models import Token


class GetAuthTokenSerializer(CustomSerializer):
    email = serializers.EmailField(error_messages={
        'required': 'Required data',
        'invalid': 'Invalid data',
    })
    password = serializers.CharField(error_messages={
        'required': 'Required data',
        'invalid': 'Invalid data',
    })

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Inactive user')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Incorrect email or password')
        else:
            raise serializers.ValidationError('Required data')

        return attrs


class RefreshAuthTokenSerializer(CustomSerializer):
    token = serializers.CharField(error_messages={
        'required': 'Required data',
        'invalid': 'Invalid data',
    })
    refresh_token = serializers.CharField(error_messages={
        'required': 'Required data',
        'invalid': 'Invalid data',
    })

    def validate(self, attrs):
        token = attrs.get('token')
        refresh_token = attrs.get('refresh_token')

        try:
            token = Token.objects.get(key=token)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid token')

        if refresh_token != token.rkey:
            raise serializers.ValidationError('Invalid refresh token')

        attrs['token'] = token
        return attrs