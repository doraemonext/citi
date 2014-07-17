# -*- coding: utf-8 -*-

from django.db.models.signals import post_syncdb

import system.settings.models
from system.settings.models import Settings


def settings_initial(sender, **kwargs):
    Settings.objects.create(name='title', value=u'好味道众筹')
    Settings.objects.create(name='description', value=u'好味道众筹的描述')
    Settings.objects.create(name='keywords', value=u'好味道众筹的关键字')

post_syncdb.connect(settings_initial, sender=system.settings.models)