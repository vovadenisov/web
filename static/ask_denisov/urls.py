from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask_denisov.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello wordl/', include('hello_world.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace="main")),

)
