from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.db.models.fields import BooleanField
    

class JoinInUser(models):
    '''
    extending the django.contrib.auth.models.User
    by using a OneToOneField(User) property
    '''
    user=models.OneToOneField(User,null=False)
    phone=models.CharField(max_length=20,null=True)
    phone_public=models.BooleanField() 
    profile_img=models.ImageField(upload_to=user.username)
    system_notification=models.BooleanField()
    
    
class JoinInGroup(models):
    '''Group for Join in system. different with the auth.Group
    '''
    name=models.CharField(max_length=15)
    create_date=models.DateField()
    invitations=ManyToManyField(JoinInUser)
    appliers=ManyToManyField(JoinInUser)
    users=ManyToManyField(JoinInUser)
    public=BooleanField()#if the group is free to apply to join without the creator's permission.'
    creator=OneToOneField(JoinInUser)
    
#append to class declaration of JoinInUser to avoid circular dependency
JoinInUser.groups=ManyToManyField(JoinInGroup)