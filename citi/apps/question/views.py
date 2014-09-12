# -*- coding: utf-8 -*-

import logging

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView, DetailView, ListView
from sorl.thumbnail import get_thumbnail
from django_filters.views import FilterView

from apps.image.models import Image
from system.settings.models import Settings
from system.settings.views import get_setting_dict
from libs.ajax.views import AjaxResponseMixin
from .models import *
from .filter import *


logger = logging.getLogger(__name__)


class QuestionListView(FilterView):
    """
    显示项目列表页

    """
    model = Question
    filterset_class = QuestionFilter
    template_name = 'question/question_list.jinja'
    context_object_name = 'questions'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['config'] = Settings.manager.get_setting_dict()
        return context


class QuestionDetailView(DetailView):
    """
    显示项目详细信息页

    """
    model = Question
    template_name = 'question/question_detail.jinja'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['config'] = Settings.manager.get_setting_dict()
        return context