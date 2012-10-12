'''
Created on 25/09/2012

@author: siqi
'''
from django.contrib import admin
from JOININ.accounts.models import *
admin.site.register(JoinInUser)
admin.site.register(JoinInGroup)