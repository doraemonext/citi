# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from sorl.thumbnail import get_thumbnail

from apps.image.models import Image
from apps.crowdfunding.models import Project, ProjectCategory
from system.settings.models import Settings


class HomeView(TemplateView):
    """
    显示首页

    """
    template_name = 'home/home.jinja'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['config'] = Settings.manager.get_setting_dict()
        context['categories'] = ProjectCategory.objects.all()
        context['local_projects'] = Project.objects.filter(status__gt=3).order_by('-post_datetime')[:4]
        for project in context['local_projects']:
            project.image = get_thumbnail(Image.objects.get(pk=project.cover).image, '239x200', crop='center').url
        context['today_best'] = []
        for category in context['categories']:
            try:
                context['today_best'].append(Project.objects.filter(category=category).filter(status__gt=3).order_by('-attention_count')[0])
                context['today_best'][-1].image = get_thumbnail(Image.objects.get(pk=context['today_best'][-1].cover).image, '560x400', crop='center').url
            except IndexError:
                pass
        context['hot_projects'] = Project.objects.filter(status__gt=3).order_by('-attention_count')[:4]
        for project in context['hot_projects']:
            project.image = get_thumbnail(Image.objects.get(pk=project.cover).image, '239x200', crop='center').url
        context['latest_projects'] = Project.objects.filter(status__gt=3).order_by('-post_datetime')[:4]
        for project in context['latest_projects']:
            project.image = get_thumbnail(Image.objects.get(pk=project.cover).image, '239x200', crop='center').url
        return context