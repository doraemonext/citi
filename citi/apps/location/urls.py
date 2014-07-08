# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import LocationList


urlpatterns = patterns('',
    url(r'^get_provinces/$', LocationList.as_view()),
)
