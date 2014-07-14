# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from libs.api.utils import api_error_message
from .models import Location
from .serializers import LocationSerializer


class LocationProvinceList(APIView):
    """
    列出省列表

    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        province = Location.objects.filter(level=0).order_by('order')
        serializer = LocationSerializer(province, many=True)
        return Response(serializer.data)


class LocationCityList(APIView):
    """
    列出市列表

    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, province_id, format=None):
        try:
            province = Location.objects.get(pk=province_id)
        except ObjectDoesNotExist:
            return Response(api_error_message('Invalid ID'), status.HTTP_400_BAD_REQUEST)

        if province.level != 0:
            return Response(api_error_message('Invalid ID'), status.HTTP_400_BAD_REQUEST)

        city = province.get_children().order_by('order')
        serializer = LocationSerializer(city, many=True)
        return Response(serializer.data)


class LocationCountryList(APIView):
    """
    列出乡镇列表

    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, city_id, format=None):
        try:
            city = Location.objects.get(pk=city_id)
        except ObjectDoesNotExist:
            return Response(api_error_message('Invalid ID'), status.HTTP_400_BAD_REQUEST)

        if city.level != 1:
            return Response(api_error_message('Invalid ID'), status.HTTP_400_BAD_REQUEST)

        country = city.get_children().order_by('order')
        serializer = LocationSerializer(country, many=True)
        return Response(serializer.data)