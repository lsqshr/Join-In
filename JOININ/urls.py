from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','JOININ.accounts.views.login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/',include('JOININ.accounts.urls')),
    url(r'^message_wall/',include('JOININ.message_wall.urls')),
    url(r'^notification/',include('JOININ.notification.urls')),
)
