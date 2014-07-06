# -*- coding: utf-8 -*-

from django.contrib.sites.models import RequestSite
from django.views.generic.base import TemplateView
from registration import signals
from registration.views import RegistrationView as BaseRegistrationView

from .models import CustomRegistrationProfile
from .forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    """
    注册页面相关内容

    """
    template_name = 'registration_form.html'
    form_class = RegistrationForm

    def register(self, request, **cleaned_data):
        """
        处理注册表单数据

        """
        email, nickname, password = cleaned_data['email'], cleaned_data['nickname'], cleaned_data['password1']
        site = RequestSite(request)
        new_user = CustomRegistrationProfile.objects.create_inactive_user(email, nickname, password, site)
        signals.user_registered.send(sender=self.__class__, user=new_user, request=request)
        return new_user

    def get_success_url(self, request=None, user=None):
        """
        返回注册成功页面的name名称

        """
        return 'registration_complete'


class ActivationView(TemplateView):
    """
    激活页面显示

    """
    http_method_names = ['get']
    template_name = 'registration_activation.html'

    def __init__(self):
        self.is_activate = False
        super(ActivationView, self).__init__()

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
            self.is_activate = True
        else:
            self.is_activate = False
        return super(ActivationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActivationView, self).get_context_data(**kwargs)
        context['is_activate'] = self.is_activate
        return context

    def activate(self, request, activation_key):
        activated_user = CustomRegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=request)
        return activated_user