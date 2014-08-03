# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

from .views import LocationProvinceList, LocationCityList, LocationCountryList


urlpatterns = patterns('',
    url(r'^province/$', LocationProvinceList.as_view()),
    url(r'^city/(?P<province_id>[0-9]+)/$', LocationCityList.as_view()),
    url(r'^country/(?P<city_id>[0-9]+)/$', LocationCountryList.as_view()),
)
