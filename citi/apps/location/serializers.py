# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    地理位置序列化

    """
    class Meta:
        model = Location
        fields = ('id', 'name')