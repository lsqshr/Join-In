'''
Created on 25/09/2012

@author: siqi
'''
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<scope>private)/(?P<action>\b(view|apply)\b)/$', 'JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>private)/(?P<action>\b(accept|deny)\b)/(?P<group_id>\d+)/$', 'JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>private)/(?P<action>view)/notification_set_read/(?P<notification_id>\d+)/$','JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>private)/(?P<action>view)/(?P<see>\b(all_notifications|unread_notifications)\b)/$','JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>private)/(?P<action>view)/(?P<mark>\b(mark_as_read|mark_as_unread)\b)/(?P<message_id>\d+)/$','JOININ.message_wall.views.mark_read'),
    url(r'^(?P<scope>group)/(?P<group_id>\d+)/(?P<action>\b(view|invite|leave)\b)/$', 'JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>group)/(?P<group_id>\d+)/(?P<action>\b(accept|deny)\b)/(?P<username>\b([a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,4})\b)/$', 'JOININ.message_wall.views.message_wall'),
    url(r'^(?P<scope>group)/(?P<group_id>\d+)/view/(?P<mark>\b(mark_as_read|mark_as_unread)\b)/(?P<message_id>\d+)/$', 'JOININ.message_wall.views.mark_read'),
)