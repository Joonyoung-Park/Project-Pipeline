from django.conf.urls import patterns, url
from pipeline import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^data_input/$', views.data_input, name='data_input'),
                       url(r'^project_status/$', views.project_status, name='project_status'),
                       url(r'^project_modify/$', views.project_modify, name='project_modify'),
                       url(r'^(?P<pipeline_id>\d+)/detail/$', views.detail, name='detail')
                       )
