from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0], 'path': 'index.html'}),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('main.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
