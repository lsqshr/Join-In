from JOININ.accounts.models import JoinInUser, JoinInGroup
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

    def __unicode__(self):    
        return 'from:'+self.written_by+'content:'+self.content
    #methods
    def add_url(self,url):
        self.web_url=url
        return
    
    def add_file(self, file):
        self.file = file
        return
    
    def set_priority(self, p):
        self.priority = p
        return
    
    def set_datetime(self):
        self.send_datetime = datetime.datetime.now()
        return
    
    def enter_content(self, c):
        self.content = c
        return

class PrivateMessage(models.Model):
    '''
    The private status of a certain message for a user. 
    It is generated for all the relevant people when a message is sent.
    '''
    
    message=models.ForeignKey(Message,related_name='private_messages')
    belongs_to=models.ForeignKey(JoinInUser,related_name='private_messages')
    read=models.BooleanField(default=False)
    priorty=models.CharField(max_length=1)
    trashed=models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'private message to:' + self.message.content
        
    def get_messages(self,user_id,group_id):
        joinin_user=User.objects.get(id=user_id).JoinInUser
        if group_id:
            return joinin_user.private_messages.order_by('message__send_datetime')
        else:
            return joinin_user.private_messages.filter(message__belongs_to_group__id=group_id)\
                .order_by('message__send_datetime')
       
    
class File(models.Model):
    name = models.CharField(max_length=20)
    last_edited = models.DateTimeField()
    uploaded_by = models.ForeignKey(JoinInUser)
    belongs_to_group = models.ForeignKey(JoinInGroup)
    message=models.ForeignKey(Message,null=False,related_name='files')
    
    def set_name(self, n):
        self.name = n
        return
    
    def update_time(self):
        self.last_edited = datetime.datetime.now()
        return    
    