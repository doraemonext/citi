# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, DjangoFilterBackend, OrderingFilter

from libs.api import mixins
from libs.api import utils
from libs.exceptions import AlreadyOperationException
from .models import (
    ProjectCategory, Project, ProjectFeedback, ProjectPackage, ProjectAttention, ProjectComment,
    ProjectTopic, ProjectTopicComment, ProjectSupport, ProjectSection
)
from .serializers import (
    ProjectCategorySerializer, ProjectSerializer, ProjectFeedbackSerializer, ProjectPackageSerializer,
    ProjectCommentSerializer, ProjectTopicSerializer, ProjectTopicCommentSerializer, ProjectSectionSerializer
)


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
                  mixins.CustomListModelMixin,
                  generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('id', 'user', 'name', 'location', 'category', 'status', 'post_datetime')
    search_fields = ('name', )
    ordering_fields = ('post_datetime', 'name', 'attention_count')
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


class ProjectSave(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, project_id, format=None):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return utils.CommonResponse.not_found()
        project.save_project()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class ProjectAttentionDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, project_id, format=None):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return utils.CommonResponse.not_found()

        if ProjectAttention.manager.is_attention(project, request.user):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, project_id, format=None):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return utils.CommonResponse.not_found()

        ProjectAttention.manager.attention(project, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, project_id, format=None):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return utils.CommonResponse.not_found()

        ProjectAttention.manager.inattention(project, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCommentList(mixins.CustomCreateModelMixin,
                         mixins.CustomListModelMixin,
                         generics.GenericAPIView):
    queryset = ProjectComment.objects.all()
    serializer_class = ProjectCommentSerializer
    permission_classes = (permissions.AllowAny, )
    paginate_by = 10

    def __init__(self):
        self.project = None
        super(ProjectCommentList, self).__init__()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(project=self.kwargs['project_id'])
        queryset = queryset.filter(parent=None)
        return super(ProjectCommentList, self).filter_queryset(queryset)

    def pre_save(self, obj):
        obj.project = self.project

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)

        return self.create(request, *args, **kwargs)


class ProjectCommentDetail(mixins.CustomRetrieveModelMixin,
                           mixins.CustomUpdateModelMixin,
                           mixins.CustomDestroyModelMixin,
                           generics.GenericAPIView):
    queryset = ProjectComment.objects.all()
    serializer_class = ProjectCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def check_object_permissions(self, request, obj):
        if request.method not in permissions.SAFE_METHODS and request.user != obj.user:
            self.permission_denied(request)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectTopicList(mixins.CustomCreateModelMixin,
                       mixins.CustomListModelMixin,
                       generics.GenericAPIView):
    queryset = ProjectTopic.objects.all()
    serializer_class = ProjectTopicSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('id', 'user', 'title')
    search_fields = ('title', )
    ordering_fields = ('post_datetime', 'title')
    paginate_by = 10

    def __init__(self):
        self.project = None
        super(ProjectTopicList, self).__init__()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(project=self.kwargs['project_id'])
        return super(ProjectTopicList, self).filter_queryset(queryset)

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.project = self.project

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)

        return self.create(request, *args, **kwargs)


class ProjectTopicDetail(mixins.CustomRetrieveModelMixin,
                         mixins.CustomUpdateModelMixin,
                         mixins.CustomDestroyModelMixin,
                         generics.GenericAPIView):
    queryset = ProjectTopic.objects.all()
    serializer_class = ProjectTopicSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        if request.method not in permissions.SAFE_METHODS:
            if request.user != obj.user:
                self.permission_denied(request)
        else:
            if not ProjectSupport.manager.has_support(obj.project, request.user):
                self.permission_denied(request)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectTopicCommentList(mixins.CustomCreateModelMixin,
                              mixins.CustomListModelMixin,
                              generics.GenericAPIView):
    queryset = ProjectTopicComment.objects.all()
    serializer_class = ProjectTopicCommentSerializer
    permission_classes = (permissions.IsAuthenticated, )
    paginate_by = 10

    def __init__(self):
        self.topic = None
        super(ProjectTopicCommentList, self).__init__()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(topic=self.kwargs['topic_id'])
        queryset = queryset.filter(parent=None)
        return super(ProjectTopicCommentList, self).filter_queryset(queryset)

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.topic = self.topic
        obj.project = self.topic.project

    def get(self, request, *args, **kwargs):
        try:
            self.topic = ProjectTopic.objects.get(pk=self.kwargs['topic_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.topic = ProjectTopic.objects.get(pk=self.kwargs['topic_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)

        return self.create(request, *args, **kwargs)


class ProjectTopicCommentDetail(mixins.CustomRetrieveModelMixin,
                                mixins.CustomUpdateModelMixin,
                                mixins.CustomDestroyModelMixin,
                                generics.GenericAPIView):
    queryset = ProjectTopicComment.objects.all()
    serializer_class = ProjectTopicCommentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        if request.method not in permissions.SAFE_METHODS:
            if request.user != obj.user:
                self.permission_denied(request)
        else:
            if not ProjectSupport.manager.has_support(obj.project, request.user):
                self.permission_denied(request)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectSectionList(mixins.CustomListModelMixin,
                         mixins.CustomCreateModelMixin,
                         generics.GenericAPIView):
    queryset = ProjectSection.objects.all()
    serializer_class = ProjectSectionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def __init__(self):
        self.project = None
        super(ProjectSectionList, self).__init__()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(project=self.kwargs['project_id'])
        return super(ProjectSectionList, self).filter_queryset(queryset)

    def pre_save(self, obj):
        obj.project = self.project

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['project_id'])
        except ObjectDoesNotExist:
            return Response(utils.api_error_message('Not found'), status=status.HTTP_404_NOT_FOUND)
        if self.project.user != request.user:
            return utils.CommonResponse.forbidden()

        return self.create(request, *args, **kwargs)