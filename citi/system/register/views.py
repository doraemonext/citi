# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import RequestSite
from registration import signals
from registration.views import RegistrationView as BaseRegistrationView
from registration.views import ActivationView as BaseActivationView

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


        """
        email, nickname, password = cleaned_data['email'], cleaned_data['nickname'], cleaned_data['password1']
        site = RequestSite(request)
        new_user = CustomRegistrationProfile.objects.create_inactive_user(email, nickname, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        判断当前是否允许注册

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('registration_complete', (), {})


class ActivationView(BaseActivationView):
    template_name = 'registration_activate.html'

    def activate(self, request, activation_key):
        """
        激活账户页面

        """
        activated_user = CustomRegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})
