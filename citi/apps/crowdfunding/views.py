# -*- coding: utf-8 -*-

import logging

from django.views.generic import TemplateView, CreateView

from .models import Project


logger = logging.getLogger(__name__)


class PublishView(TemplateView):
    template_name = 'crowdfunding/publish.html'

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['agreement'] = u'发布项目协议'
        return context


class PublishContentView(CreateView):
    model = Project
    template_name_suffix = '_create_form'
    fields = ['name', 'location', 'location_detail', 'category', 'total_money', 'total_days',
              'summary', 'content']

