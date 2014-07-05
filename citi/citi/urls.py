from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from apps.location import views as location_views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('system.users.urls')),
    url(r'^captcha/', include('captcha.urls')),

    # Examples:
    # url(r'^$', 'citi.views.home', name='home'),
    # url(r'^citi/', include('citi.foo.urls')),

    url(r'^api/location/$', location_views.LocationList.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
urlpatterns = format_suffix_patterns(urlpatterns)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
