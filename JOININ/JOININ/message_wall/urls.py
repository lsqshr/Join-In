'''
Created on 25/09/2012

@author: siqi
'''
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<link>\b(view|apply)\b)/$', 'JOININ.message_wall.views.private_message_wall'),
    url(r'^(?P<link>\b(accept|deny)\b)/(?P<group_id>\d+)/$', 'JOININ.message_wall.views.private_message_wall'),
    url(r'^group/(?P<group_id>\d+)/(?P<link>\b(view|invite|leave)\b)/$', 'JOININ.message_wall.views.group_message_wall'),
    url(r'^group/(?P<link>\b(accept|deny)\b)/(?P<user_id>\d+)/$', 'JOININ.message_wall.views.private_message_wall'),
)