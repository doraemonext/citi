# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import login as views_login, logout as views_logout


urlpatterns = patterns('',
    url(r'^login/$', views_login, name='login'),
    url(r'^logout/$', views_logout, name='logout'),
    #url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    #url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    #url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    #url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
)
