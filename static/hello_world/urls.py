from django.conf.urls import patterns, url

from hello_world import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
