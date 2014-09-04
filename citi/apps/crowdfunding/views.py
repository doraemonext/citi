# -*- coding: utf-8 -*-

import logging

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView, DetailView
from sorl.thumbnail import get_thumbnail

from system.settings.views import get_setting_dict
from libs.ajax.views import AjaxResponseMixin
from .forms import ProjectForm
from .models import Project


logger = logging.getLogger(__name__)


class ProjectDetailView(DetailView):
    """
    显示项目详细信息页

    """
    model = Project
    template_name = 'crowdfunding/project_detail.jinja'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['user_image'] = get_thumbnail(self.object.user.detailinfo.avatar.image, '100x100', crop='center').url
        return context


class PublishView(TemplateView):
    """
    发布项目 - 显示协议页面

    """
    template_name = 'crowdfunding/publish.html'

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['agreement'] = get_setting_dict('publish_agreement')
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PublishView, self).dispatch(request, *args, **kwargs)


class PublishContentView(AjaxResponseMixin, FormView):
    """
    发布项目 - 填写项目基本信息

    """
    template_name = 'crowdfunding/publish_content.html'
    http_method_names = ['get', 'post']
    form_class = ProjectForm

    def __init__(self):
        self.object = None
        super(PublishContentView, self).__init__()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return super(PublishContentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('crowdfunding.publish.payoff', kwargs={'project_id': self.object.pk})

    @method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PublishContentView, self).dispatch(request, *args, **kwargs)


class PublishPayoffView(TemplateView):
    """
    发布项目 - 填写项目相关报酬回馈信息

    """
    template_name = 'crowdfunding/publish_payoff.html'
    http_method_names = ['get']

    def __init__(self):
        self.project = None
        super(PublishPayoffView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=kwargs['project_id'])
        except KeyError:
            raise Http404
        except ObjectDoesNotExist:
            raise Http404
        return super(PublishPayoffView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PublishPayoffView, self).dispatch(request, *args, **kwargs)


class PublishVerifyView(TemplateView):
    """
    发布项目 - 最后预览界面

    """
    template_name = 'crowdfunding/publish_payoff.html'
    http_method_names = ['get']

    def __init__(self):
        self.project = None
        super(PublishVerifyView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=kwargs['project_id'])
        except KeyError:
            raise Http404
        except ObjectDoesNotExist:
            raise Http404
        return super(PublishVerifyView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PublishVerifyView, self).dispatch(request, *args, **kwargs)