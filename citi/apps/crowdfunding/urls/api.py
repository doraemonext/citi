# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from ..api import ProjectCategoryList
from ..api import ProjectList, ProjectDetail, ProjectAttentionDetail, ProjectSave
from ..api import ProjectCommentList, ProjectCommentDetail
from ..api import ProjectFeedbackList, ProjectFeedbackDetail
from ..api import ProjectPackageList, ProjectPackageDetail
from ..api import ProjectTopicList, ProjectTopicDetail
from ..api import ProjectTopicCommentList, ProjectTopicCommentDetail
from ..api import ProjectSectionList, ProjectSectionDetail


urlpatterns = patterns('',
    url(r'^category/$', ProjectCategoryList.as_view()),
    url(r'^project/$', ProjectList.as_view()),
    url(r'^project/(?P<pk>[0-9]+)/$', ProjectDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/save/$', ProjectSave.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/attention/$', ProjectAttentionDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/comment/$', ProjectCommentList.as_view()),
    url(r'^project/comment/(?P<pk>[0-9]+)/$', ProjectCommentDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/topic/$', ProjectTopicList.as_view()),
    url(r'^project/topic/(?P<pk>[0-9]+)/$', ProjectTopicDetail.as_view()),
    url(r'^project/topic/(?P<topic_id>[0-9]+)/comment/$', ProjectTopicCommentList.as_view()),
    url(r'^project/topic/comment/(?P<pk>[0-9]+)/$', ProjectTopicCommentDetail.as_view()),
    url(r'^project/(?P<project_id>[0-9]+)/section/$', ProjectSectionList.as_view()),
    url(r'^project/section/(?P<pk>[0-9]+)/$', ProjectSectionDetail.as_view()),
    url(r'^feedback/$', ProjectFeedbackList.as_view()),
    url(r'^feedback/(?P<pk>[0-9]+)/$', ProjectFeedbackDetail.as_view()),
    url(r'^package/$', ProjectPackageList.as_view()),
    url(r'^package/(?P<pk>[0-9]+)/$', ProjectPackageDetail.as_view()),
)
