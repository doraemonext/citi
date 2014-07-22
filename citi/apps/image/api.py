# -*- coding: utf-8 -*-

import logging

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from libs.api import mixins
from .models import Image
from .serializers import ImageSerializer


logger = logging.getLogger(__name__)


class ImageList(mixins.CustomCreateModelMixin,
                generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny, )

    def pre_save(self, obj):
        if self.request.user.is_authenticated():
            obj.user = self.request.user
        else:
            obj.user = None

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ImageDetail(mixins.CustomRetrieveModelMixin,
                  mixins.CustomUpdateModelMixin,
                  mixins.CustomDestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny, )

    def pre_save(self, obj):
        if self.request.user.is_authenticated():
            obj.user = self.request.user
        else:
            obj.user = None

    def check_object_permissions(self, request, obj):
        if request.method != 'GET':
            if obj.user:
                if not request.user.is_authenticated() or request.user != obj.user:
                    raise PermissionDenied()
        super(ImageDetail, self).check_object_permissions(request, obj)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)