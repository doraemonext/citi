# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Location(MPTTModel):
    """
    城市位置 model

    """
    name = models.CharField(u'城市名称', max_length=20)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'父级城市')

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = u"地理位置"
        verbose_name_plural = u"地理位置"