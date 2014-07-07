# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .views import RegistrationView, ActivationView
from .views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration_complete.html'), name='registration_complete'),
    url(r'^register/activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password_reset/confirm/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset/complete/$', password_reset_complete, name='password_reset_complete'),
    #url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    #url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
)
