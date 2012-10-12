'''
Created on 25/09/2012

@author: siqi
'''
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'JOININ.message_wall.views.private_message_wall'),
    url(r'^group/(?P<group_id>\d+)/(?P<link>\b(view|invite|leave)\b)/$', 'JOININ.message_wall.views.group_message_wall'),
)
