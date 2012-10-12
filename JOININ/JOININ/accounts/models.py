from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ManyToManyField, OneToOneField, ForeignKey
import datetime
from JOININ.JOININ.message_wall.models import JoinInFile
    
class JoinInUserManager(models.Manager):
    def create_user(self, email, password):
        new_user = User.objects.create(username=email, email=email)
        new_user.set_password(password)
        new_user.save()
        new_joinin_user=self.create(user=new_user) 
        return new_joinin_user

class JoinInUser(models.Model):
    '''
    extending the django.contrib.auth.models.User
    by using a OneToOneField(User) property
    '''
    #vars
    user = models.OneToOneField(User, null=False,unique=True,related_name='joinin_user')
    phone = models.CharField(max_length=20, null=True,blank=True)
    phone_public = models.BooleanField(default=False) 
    profile_img = models.ImageField(upload_to='profile_imgs',null=True,blank=True)
    system_notification = models.BooleanField(default=True)
    email_update = BooleanField(default=True)
    objects=JoinInUserManager() 
    last_login=models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return 'JoinInUser for:'+ self.user.username
    
class JoinInGroup(models.Model):
    '''Group for Join in system. different with the auth.Group
    '''
    name = models.CharField(max_length=15)
    create_datetime = models.DateTimeField()
    invitations = ManyToManyField(JoinInUser, null=True,related_name="groups_invites")
    appliers = ManyToManyField(JoinInUser, null=True,related_name="groups_to_apply")
    users = ManyToManyField(JoinInUser, null=True,related_name="groups")
    public = BooleanField(default=False)#if the group is free to apply to join without the creator's permission.'
    creator = ForeignKey(JoinInUser,related_name='created_groups')
    
    def __unicode__(self):
        return self.name
    
    def get_files(self):
        f = JoinInFile.objects.get(belongs_to_group=self.name)
        return f
        
        
    
class Feedback(models.Model):
    send_datetime = models.DateTimeField()
    written_by = models.ForeignKey(JoinInUser,related_name='feedbacks')
    content = models.CharField(max_length=1000)
