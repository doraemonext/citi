# -*- coding: utf-8 -*-

import logging

#from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from .forms import ProjectForm


logger = logging.getLogger(__name__)


class PublishView(TemplateView):
    template_name = 'crowdfunding/publish.html'

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['agreement'] = u'发布项目协议'
        return context


class PublishContentView(FormView):
    template_name = 'crowdfunding/publish_content.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        project.save()
        return HttpResponseRedirect(self.get_success_url(project.pk))

    def get_success_url(self, project_id=None):
        return '/' + str(project_id) + '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PublishContentView, self).dispatch(request, *args, **kwargs)