'''
Created on 25/09/2012

@author: siqi
'''
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'JOININ.views.home', name='home'),
    # url(r'^JOININ/', include('JOININ.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$','JOININ.accounts.views.login'),
    url(r'^signup/$','JOININ.accounts.views.signup'),
)
