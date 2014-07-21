# -*- coding: utf-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from libs.api import mixins
from .models import ProjectFeedback, ProjectPackage
from .serializers import ProjectFeedbackSerializer, ProjectPackageSerializer


logger = logging.getLogger(__name__)


class ProjectFeedbackList(mixins.CustomCreateModelMixin,
                          generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def pre_save(self, obj):
        if self.request.user != obj.project.user:
            raise PermissionDenied()
        super(ProjectFeedbackList, self).pre_save(obj)

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.add_projectfeedback'):
            raise PermissionDenied()
        return self.create(request, *args, **kwargs)


class ProjectFeedbackDetail(mixins.CustomRetrieveModelMixin,
                            mixins.CustomUpdateModelMixin,
                            mixins.CustomDestroyModelMixin,
                            generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        if request.user != obj.project.user:
            self.permission_denied(request)
        super(ProjectFeedbackDetail, self).check_object_permissions(request, obj)

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.view_projectfeedback'):
            raise PermissionDenied()
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.change_projectfeedback'):
            raise PermissionDenied()
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.change_projectfeedback'):
            raise PermissionDenied()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.delete_projectfeedback'):
            raise PermissionDenied()
        return self.destroy(request, *args, **kwargs)


class ProjectPackageList(mixins.CustomCreateModelMixin,
                         generics.GenericAPIView):
    queryset = ProjectPackage.objects.all()
    serializer_class = ProjectPackageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectPackageDetail(mixins.CustomRetrieveModelMixin,
                           mixins.CustomUpdateModelMixin,
                           mixins.CustomDestroyModelMixin,
                           generics.GenericAPIView):
    queryset = ProjectPackage.objects.all()
    serializer_class = ProjectPackageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)