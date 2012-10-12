from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JOININ.views.home', name='home'),
    # url(r'^JOININ/', include('JOININ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/',include('JOININ.accounts.urls')),
    url(r'^message_wall/',include('JOININ.message_wall.urls')),
    url(r'^hi/','JOININ.message_wall.views.hi'),
    
)
