# -*- coding: utf-8 -*-

import xadmin

from .models import Location


class LocationAdmin(object):
    pass


xadmin.site.register(Location, LocationAdmin)