# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from rest_framework import serializers

from libs.api.serializers import CustomSerializer


class AuthTokenSerializer(CustomSerializer):
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
