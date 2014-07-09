# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import GetObtainAuthToken, RefreshObtainAuthToken


urlpatterns = patterns('',
    url(r'^get/$', GetObtainAuthToken.as_view()),
    url(r'^refresh/$', RefreshObtainAuthToken.as_view()),
)
