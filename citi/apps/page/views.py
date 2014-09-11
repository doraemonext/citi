# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView


class AgreementView(TemplateView):
    template_name = 'page/agreement.jinja'


class ContactView(TemplateView):
    template_name = 'page/contact.jinja'


class CopyrightView(TemplateView):
    template_name = 'page/copyright.jinja'


class DisclaimerView(TemplateView):
    template_name = 'page/disclaimer.jinja'


class FeedbackView(TemplateView):
    template_name = 'page/feedback.jinja'