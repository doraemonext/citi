# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView

from libs.ajax.views import AjaxResponseMixin
from .forms import ProjectForm


logger = logging.getLogger(__name__)


class PublishView(TemplateView):
    template_name = 'crowdfunding/publish.html'

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['agreement'] = u'发布项目协议'
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PublishView, self).dispatch(request, *args, **kwargs)


class PublishContentView(AjaxResponseMixin, FormView):
    template_name = 'crowdfunding/publish_content.html'
    form_class = ProjectForm

    def __init__(self):
        self.object = None
        super(PublishContentView, self).__init__()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PublishContentView, self).form_valid(form)

    def get_success_url(self):
        url = '/crowdfunding/publish/payoff/' + str(self.object.pk) + '/'  # DEBUG用, 需修改
        return url

    @method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PublishContentView, self).dispatch(request, *args, **kwargs)