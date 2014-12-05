from django.conf.urls import patterns, include, url
from django.contrib import admin

import bleats.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', bleats.views.homepage, name='homepage'),
    url(r'^timeline/(?P<shortname>\w+)$', bleats.views.timeline, name='timeline'),
    url(r'^create$', bleats.views.create_bleat, name='create_bleat'),
    url(r'^toggle_following$', bleats.views.toggle_following, name='toggle_following'),
)
