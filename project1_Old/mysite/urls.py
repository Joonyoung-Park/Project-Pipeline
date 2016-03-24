from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^pipeline/', include('pipeline.urls', namespace="pipeline")),
	url(r'^admin/', include(admin.site.urls)),
)