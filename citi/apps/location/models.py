# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Location(MPTTModel):
    """
    地理位置 model

    """
    name = models.CharField(u'城市名称', max_length=20)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'父级城市')
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = u"地理位置"
        verbose_name_plural = u"地理位置"
        permissions = (
            ('view_location', u'Can view 地理位置'),
        )

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
        Location.objects.rebuild()

    def __unicode__(self):
        return self.name