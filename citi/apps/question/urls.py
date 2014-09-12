# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .views import QuestionListView, QuestionDetailView, question_create, question_answer_create


urlpatterns = patterns('',
    url(r'^list/$', QuestionListView.as_view(), name='question.list'),
    url(r'^list/create/$', question_create, name='question.list.create'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', QuestionDetailView.as_view(), name='question.detail'),
    url(r'^detail/(?P<pk>[-_\w]+)/create/$', question_answer_create, name='question.detail.create'),
)
