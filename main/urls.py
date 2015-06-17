from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^question/(?P<quest>\d+)/$', views.question, name='question'),
    url(r'^user/$', views.user, name='user'),
    #url(r'^register/$', views.register, name='register'),
    url(r'^', views.main, name='main'),
)
