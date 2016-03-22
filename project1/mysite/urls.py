from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(
                           r'^accounts/login/',
                           'django.contrib.auth.views.login',
                           name='login',
                           kwargs={
                               'template_name': 'login.html'
                           }
                       ),
                       url(
                           r'^accounts/logout/',
                           'django.contrib.auth.views.logout',
                           name='logout'
                       ),
                       url(
                           r'^pipeline/',
                           include('pipeline.urls', namespace="pipeline")
                       ),
                       url(
                           r'^admin/',
                           include(admin.site.urls)),
                       )
