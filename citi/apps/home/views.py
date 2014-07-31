# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView


class HomeView(TemplateView):
    """
    显示首页

    """
    template_name = 'home/home.html'