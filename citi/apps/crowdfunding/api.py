# -*- coding: utf-8 -*-

import logging

from rest_framework import generics

from libs.api import mixins
from .models import ProjectFeedback, ProjectPackage
from .serializers import ProjectFeedbackSerializer, ProjectPackageSerializer


class ProjectFeedbackList(mixins.CustomCreateModelMixin,
                          generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectFeedbackDetail(mixins.CustomRetrieveModelMixin,
                            mixins.CustomUpdateModelMixin,
                            mixins.CustomDestroyModelMixin,
                            generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectPackageList(mixins.CustomCreateModelMixin,
                         generics.GenericAPIView):
    queryset = ProjectPackage.objects.all()
    serializer_class = ProjectPackageSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectPackageDetail(mixins.CustomRetrieveModelMixin,
                           mixins.CustomUpdateModelMixin,
                           mixins.CustomDestroyModelMixin,
                           generics.GenericAPIView):
    queryset = ProjectPackage.objects.all()
    serializer_class = ProjectPackageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)