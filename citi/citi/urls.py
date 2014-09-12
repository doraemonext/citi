from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from apps.home.views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('apps.account.urls.web')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^crowdfunding/', include('apps.crowdfunding.urls.web')),
    url(r'^static_page/', include('apps.page.urls')),
    url(r'^question/', include('apps.question.urls')),

    url(r'^api/', include([
        url(r'^token/', include('system.authtoken.urls')),
        url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^image/', include('apps.image.urls.api')),
        url(r'^location/', include('apps.location.urls')),
        url(r'^accounts/', include('apps.account.urls.api')),
        url(r'^crowdfunding/', include('apps.crowdfunding.urls.api')),
    ])),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns = format_suffix_patterns(urlpatterns)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)