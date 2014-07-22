# -*- coding: utf-8 -*-

import logging

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from libs.api import fields
from .models import Image


logger = logging.getLogger(__name__)


class ImageSerializer(serializers.ModelSerializer):
    """
    图片序列化

    """
    user = fields.CustomPrimaryKeyRelatedField(read_only=True)
    type = fields.CustomIntegerField()
    image = fields.CustomImageField(write_only=True)
    url = SerializerMethodField('get_absolute_url')

    def get_absolute_url(self, obj):
        return obj.image.url

    def validate_type(self, attrs, source):
        data = attrs[source]
        for iter in Image.TYPE:
            if data == iter[0]:
                return attrs
        raise serializers.ValidationError('Invalid type')

    class Meta:
        model = Image
        fields = ('id', 'user', 'type', 'image', 'url')