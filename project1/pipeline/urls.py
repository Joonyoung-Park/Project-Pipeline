from django.conf.urls import patterns, url
from pipeline import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^data_input/$', views.data_input, name='data_input'),
                       url(r'^data_modify/$', views.data_modify, name='data_modify'),
                       #
                       url(r'^data_modify/(?P<pipeline_id>\d+)/$', views.data_modify, name='data_modify'),
                       url(r'^data_modify_save/(?P<project_code_text>\S+)/$', views.data_modify_save, name='data_modify_save'),
                       url(r'^project_status/$', views.project_status, name='project_status'),
                       url(r'^(?P<pipeline_id>\d+)/detail/$', views.detail, name='detail'),
                       )

# from django.conf.urls import patterns, url
# from pipeline import views
#
# urlpatterns = patterns('',
#                        url(r'^$', views.index, name='index'),
#                        url(r'^data_input/$', views.data_input, name='data_input'),
#                        url(r'^data_modify/$', views.data_modify, name='data_modify'),
#                        url(r'^project_status/$', views.project_status, name='project_status'),
#                        url(r'^(?P<pipeline_id>\d+)/detail/$', views.detail, name='detail'),
#                        )
