# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .views import QuestionListView, QuestionDetailView


urlpatterns = patterns('',
    url(r'^list/$', QuestionListView.as_view(), name='question.list'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', QuestionDetailView.as_view(), name='question.detail'),
)
