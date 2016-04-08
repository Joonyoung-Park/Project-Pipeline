from django.conf.urls import url

from . import views

app_name = 'pipeline'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project_status', views.project_status, name='project_status'),
    url(r'^data_input', views.data_input, name='data_input'),
    url(r'^(?P<pipeline_id>[0-9]+)/data_modify/$', views.data_modify, name='data_modify'),
]
