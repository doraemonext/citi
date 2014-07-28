# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from ..api import UserDetail, UserAnonymousDetail


urlpatterns = patterns('',
    url(r'^user/$', UserDetail.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', UserAnonymousDetail.as_view()),
)
