# -*- coding: utf-8 -*-

import logging

from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, DjangoFilterBackend, OrderingFilter

from libs.api import mixins
from .models import ProjectCategory, Project, ProjectFeedback, ProjectPackage
from .serializers import ProjectCategorySerializer, ProjectSerializer, ProjectFeedbackSerializer, ProjectPackageSerializer


logger = logging.getLogger(__name__)


class ProjectCategoryList(APIView):
    """
    列出项目分类列表

    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        province = ProjectCategory.objects.filter(level=0).order_by('order')
        serializer = ProjectCategorySerializer(province, many=True)
        return Response(serializer.data)


class ProjectList(mixins.CustomCreateModelMixin,
                  mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('id', 'user', 'name', 'location', 'category', 'status', 'post_datetime')
    search_fields = ('name', )
    ordering_fields = ('post_datetime', 'name')
    paginate_by = 10

    def pre_save(self, obj):
        if self.request.user.is_authenticated():
            obj.user = self.request.user
        else:
            obj.user = None

    def post_save(self, obj, created=False):
        if type(obj.tags) is list:
            saved_obj = Project.objects.get(pk=obj.pk)
            for tag in obj.tags:
                saved_obj.tags.add(tag)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectDetail(mixins.CustomRetrieveModelMixin,
                    mixins.CustomUpdateModelMixin,
                    mixins.CustomDestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def check_object_permissions(self, request, obj):
        if request.user != obj.user:
            self.permission_denied(request)
        super(ProjectDetail, self).check_object_permissions(request, obj)

    def post_save(self, obj, created=False):
        # 当请求为 PUT 或请求为 PATCH 并且有 tags 数据时清空原有 tags
        if self.request.method == 'PUT' or (self.request.method == 'PATCH' and type(obj.tags) is list):
            saved_obj = Project.objects.get(pk=obj.pk)
            saved_obj.tags.clear()

        if type(obj.tags) is list:
            saved_obj = Project.objects.get(pk=obj.pk)
            for tag in obj.tags:
                saved_obj.tags.add(tag)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectFeedbackList(mixins.CustomCreateModelMixin,
                          generics.GenericAPIView):
    queryset = ProjectFeedback.objects.all()
    serializer_class = ProjectFeedbackSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
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
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
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

    def check_object_permissions(self, request, obj):
        if request.user != obj.project.user:
            self.permission_denied(request)
        super(ProjectPackageDetail, self).check_object_permissions(request, obj)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)