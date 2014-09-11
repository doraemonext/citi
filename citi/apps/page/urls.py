# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

from .views import AgreementView, ContactView, CopyrightView, DisclaimerView, FeedbackView


urlpatterns = patterns('',
    url(r'^agreement/$', AgreementView.as_view(), name='page.agreement'),
    url(r'^contact/$', ContactView.as_view(), name='page.contact'),
    url(r'^copyright/$', CopyrightView.as_view(), name='page.copyright'),
    url(r'^disclaimer/$', DisclaimerView.as_view(), name='page.disclaimer'),
    url(r'^feedback/$', FeedbackView.as_view(), name='page.feedback'),
)
