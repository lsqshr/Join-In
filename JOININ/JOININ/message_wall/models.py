from JOININ.JOININ.accounts.models import JoinInUser, JoinInGroup
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ManyToManyField
import datetime



          
class Message(models.Model):
    reply_to = models.ForeignKey('self', null=True,related_name='reply')
    web_url = models.URLField(null=True)
    priority_choices = ((1, 'Low'),(2, 'Medium'),( 3, 'High'),)
    priority = models.IntegerField(choices=priority_choices, default=1)
    send_datetime = models.DateTimeField()
    send_to=models.ForeignKey(JoinInUser,related_name='one_to_one_messages',null=True)
    belongs_to_group = models.ForeignKey(JoinInGroup,related_name='messages')
    written_by = models.ForeignKey(JoinInUser,related_name='messages')
    content = models.CharField(max_length=1000)
    '''file = models.FileField(upload_to='files',null=True,blank=True) '''
    
    def __unicode__(self):
        username_str=self.written_by.user.username
        return 'from:'+username_str+'content:'+self.content

class PrivateMessage(models.Model):
    '''
    The private status of a certain message for a user. 
    It is generated for all the relevant people when a message is sent.
    '''
    
    message=models.ForeignKey(Message,related_name='private_messages')
    belongs_to=models.ForeignKey(JoinInUser,related_name='private_messages')
    read=models.BooleanField(default=False)
    priority=models.CharField(max_length=1)
    trashed=models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'private message to:' + self.message.content
       
    
class JoinInFile(models.Model):
    file = models.FileField(upload_to='files',null=True,blank=True)
    name = models.CharField(max_length=20)
    uploaded_by = models.ForeignKey(JoinInUser, null=False)
    belongs_to_group = models.ForeignKey(JoinInGroup, null=False)
    message=models.ForeignKey(Message,null=False,related_name='files')
    
    def create_file(self, name, user, group):
        self.file = open('/files', 'r+')
        self.file.save(name,' ')
        self.file.close()
        self.belongs_to_group=group
        self.uploaded_by=user
        return
    
    def rename(self, n):
        self.name = n
        return
    
    def update_time(self):
        self.last_edited = datetime.datetime.now()
        return    
    