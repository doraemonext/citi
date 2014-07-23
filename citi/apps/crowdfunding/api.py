# -*- coding: utf-8 -*-

import logging

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, DjangoFilterBackend

from libs.api import mixins
from .models import Project, ProjectFeedback, ProjectPackage
from .serializers import ProjectSerializer, ProjectFeedbackSerializer, ProjectPackageSerializer


logger = logging.getLogger(__name__)


class ProjectList(mixins.CustomCreateModelMixin,
                  mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', 'user', 'name', 'location', 'category', 'status', 'post_datetime')
    search_fields = ('name', )

    def pre_save(self, obj):
        if self.request.user.is_authenticated():
            obj.user = self.request.user
        else:
            obj.user = None

    def post_save(self, obj, created=True):
        if type(obj.tags) is list:
            saved_obj = Project.objects.get(pk=obj.pk)
            for tag in obj.tags:
                saved_obj.tags.add(tag)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.add_project'):
            raise PermissionDenied()
        return self.create(request, *args, **kwargs)


class ProjectFeedbackList(mixins.CustomCreateModelMixin,
                          generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer
    permission_classes = (permissions.IsAuthenticated, )

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
        if not request.user.has_perm('crowdfunding.add_projectpackage'):
            raise PermissionDenied()
        return self.create(request, *args, **kwargs)


class ProjectPackageDetail(mixins.CustomRetrieveModelMixin,
                           mixins.CustomUpdateModelMixin,
                           mixins.CustomDestroyModelMixin,
                           generics.GenericAPIView):
    queryset = ProjectPackage.objects.all()
    serializer_class = ProjectPackageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        if request.user != obj.project.user:
            self.permission_denied(request)
        super(ProjectPackageDetail, self).check_object_permissions(request, obj)

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.view_projectpackage'):
            raise PermissionDenied()
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.change_projectpackage'):
            raise PermissionDenied()
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.change_projectpackage'):
            raise PermissionDenied()
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm('crowdfunding.delete_projectpackage'):
            raise PermissionDenied()
        return self.destroy(request, *args, **kwargs)