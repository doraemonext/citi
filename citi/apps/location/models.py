from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Location(MPTTModel):
    name = models.CharField(max_length=20)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']