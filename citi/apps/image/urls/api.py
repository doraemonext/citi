# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from ..api import ImageList, ImageDetail


urlpatterns = patterns('',
    url(r'^$', ImageList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ImageDetail.as_view()),
)

# urlpatterns = format_suffix_patterns(urlpatterns)
