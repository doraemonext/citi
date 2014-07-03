# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Location


class LocationSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=30)
    level = serializers.IntegerField()