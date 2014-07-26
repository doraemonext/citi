# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from ..api import UserDetail


urlpatterns = patterns('',
    url(r'^user/$', UserDetail.as_view()),
)
