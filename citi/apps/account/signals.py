# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from .models import DetailInfo, FundInfo, BalanceInfo, ProjectInfo, QuestionInfo


def user_saved(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        DetailInfo.objects.create(user=user)
        FundInfo.objects.create(user=user)
        BalanceInfo.objects.create(user=user)
        ProjectInfo.objects.create(user=user)
        QuestionInfo.objects.create(user=user)

post_save.connect(user_saved, sender=get_user_model())