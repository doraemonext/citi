# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .views import PublishView, PublishContentView


urlpatterns = patterns('',
    url(r'^publish/$', PublishView.as_view(), name='crowdfunding.publish'),
    url(r'^publish/content/$', PublishContentView.as_view(), name='crowdfunding.publish.content'),
)
