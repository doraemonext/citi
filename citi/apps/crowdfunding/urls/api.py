# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from ..api import ProjectCategoryList
from ..api import ProjectList, ProjectDetail, ProjectAttentionDetail, ProjectSave
from ..api import ProjectCommentList, ProjectCommentDetail
from ..api import ProjectFeedbackList, ProjectFeedbackDetail
from ..api import ProjectPackageList, ProjectPackageDetail
from ..api import ProjectTopicList


urlpatterns = patterns('',
    url(r'^category/$', ProjectCategoryList.as_view()),
    url(r'^project/$', ProjectList.as_view()),
    url(r'^project/(?P<pk>[0-9]+)/$', ProjectDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/save/$', ProjectSave.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/attention/$', ProjectAttentionDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/comment/$', ProjectCommentList.as_view()),
    url(r'^project/comment/(?P<pk>[0-9]+)/$', ProjectCommentDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/topic/$', ProjectTopicList.as_view()),
    url(r'^feedback/$', ProjectFeedbackList.as_view()),
    url(r'^feedback/(?P<pk>[0-9]+)/$', ProjectFeedbackDetail.as_view()),
    url(r'^package/$', ProjectPackageList.as_view()),
    url(r'^package/(?P<pk>[0-9]+)/$', ProjectPackageDetail.as_view()),
)
