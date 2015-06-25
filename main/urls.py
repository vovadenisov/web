from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^question/(?P<quest>\d+)/$', views.question, name='question'),
    url(r'^user/$', views.user, name='user'),
    url(r'^register/$', views.signup, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signup/', views.signin, name='signup'),
    url(r'^add_question/', views.add, name='add_quest'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^correct/$', views.correct, name='correct'),
    url(r'^correct_email/$', views.correct_Email, name='correct_email'),
    url(r'^correct_pass/$', views.correct_password, name='correct_password'),
    url(r'^correct_Email/$', views.correct_img, name='correct_img'),
    url(r'^$', views.main, name='main'),
)
