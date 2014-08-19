# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework import response

from apps.crowdfunding.models import Project, ProjectSupport, ProjectAttention
from apps.crowdfunding.serializers import ProjectSerializer, ProjectSupportSerializer, ProjectAttentionSerializer
from libs.api import mixins
from .serializers import UserSerializer, UserAnonymousSerializer


class UserDetail(mixins.CustomRetrieveModelMixin,
                 mixins.CustomUpdateModelMixin,
                 mixins.CustomDestroyModelMixin,
                 generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def check_object_permissions(self, request, obj):
        if request.user != obj:
            self.permission_denied(request)
        super(UserDetail, self).check_object_permissions(request, obj)

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserAnonymousDetail(mixins.CustomRetrieveModelMixin,
                          generics.GenericAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserAnonymousSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserProject(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        project = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(project, many=True)
        return response.Response(serializer.data)


class UserProjectSupport(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        support = ProjectSupport.objects.filter(user=request.user)
        serializer = ProjectSupportSerializer(support, many=True)
        return response.Response(serializer.data)


class UserProjectAttention(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        attention = ProjectAttention.objects.filter(user=request.user)
        serializer = ProjectAttentionSerializer(attention, many=True)
        return response.Response(serializer.data)
