# -*- coding: utf-8 -*-

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Location
from .serializers import LocationSerializer


class LocationList(APIView):
    """
    列出所有的城市

    """
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        location = Location.objects.all()
        serializer = LocationSerializer(location, many=True)
        return Response(serializer.data)