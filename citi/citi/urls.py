from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^accounts/', include('apps.account.urls')),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^api/', include([
        url(r'^token/', 'system.authtoken.views.obtain_expiring_auth_token'),
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^location/', include('apps.location.urls')),
    ])),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns = format_suffix_patterns(urlpatterns)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
