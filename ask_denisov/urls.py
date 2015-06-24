from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_denisov.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello wordl/', include('hello_world.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace="main")),
)

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
