from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ManyToManyField, OneToOneField
import datetime
    
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
    #methods
    def join_group(self, group):
        # group is a JoinInGroup instance 
        #if this user is in the invitation list or this group is public,
        # then directly add this user to the group
        if self in group.invitations.all() or group.public:
            group.add_user(self)
        #if this user not in the invitation list, then add this user to appliers of the group
        else:
            group.add_applier(self)
        return
    
    def leave_group(self, group):
        #group is a JoinInGroup instance
        group.delete_user(self)
        return
    
    def updateInfo(self):
        self.save()
        return
    
    def change_password(self, new_password):
        #interface to change the auth.user.password
        self.user.set_password(new_password)
        return
    
    def create_group(self, group_name, create_date, invitations, public):
        #method to create a new group and set the creator to this user
        new_group = JoinInGroup.objects.create(name=group_name,
                                   create_datetime=datetime.datetime.now(), public=public, creator=self)
        #add the creator as the first user
        new_group.users.add(self) 
        return
    
    def set_email_update(self, is_update):
        self.email_update = is_update
        return
    
    def delete_account(self):
        #in this method, delete the auth.models.user binded to this user. 
        #And this record of JoinInUser will be deleted with the outer caller
        self.user.delete()
        return
    
    def change_profile_img(self, img):
        #img is a ImgField
        self.profile_img = img
        return
    
    def change_phone_num(self, new_num):
        self.phone = new_num
        return
    
    def change_email(self, new_email):
        self.user.email = new_email
        return
    
    def change_username(self, new_name):
        self.user.username = new_name
        return
    
    def change_phone_public(self, phone_public):
        self.phone_public = phone_public
        return
    
    def setTime(self):
        self.last_login = datetime.datetime.now()
        return
    
    def changeName(self, name):
        self.full_name = name
        return
    
    
class JoinInGroup(models.Model):
    '''Group for Join in system. different with the auth.Group
    '''
    name = models.CharField(max_length=15)
    create_datetime = models.DateTimeField()
    invitations = ManyToManyField(JoinInUser, null=True,related_name="groups_invites")
    appliers = ManyToManyField(JoinInUser, null=True,related_name="groups_to_apply")
    users = ManyToManyField(JoinInUser, null=True,related_name="groups")
    public = BooleanField(default=False)#if the group is free to apply to join without the creator's permission.'
    creator = OneToOneField(JoinInUser)
    
    def __unicode__(self):
        return self.name
    #methods
    def add_user(self, user):
        self.users.add(user)
        return
    def add_applier(self, user): 
        self.appliers.add(user)
        return
    def delete_user(self, user):
        self.users.remove(user)
        
#append to class declaration of JoinInUser to avoid circular dependency
#JoinInUser.groups = ManyToManyField(JoinInGroup,related_name="joinin_users")

    
class Feedback(models.Model):
    send_datetime = models.DateTimeField()
    written_by = models.ForeignKey(JoinInUser,related_name='feedbacks')
    content = models.CharField(max_length=1000)

    def set_date_time(self):
        self.send_datetime=datetime.datetime.now()
        return
    
    def enter_content(self,c):
        self.content=c
        return