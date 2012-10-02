from JOININ.accounts.models import JoinInUser, JoinInGroup
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ManyToManyField
import datetime

class File(models.Model):
    name = models.CharField(max_length=20)
    last_edited = models.DateTimeField()
    uploaded_by = models.ForeignKey(JoinInUser)
    belongs_to_group = models.ForeignKey(JoinInGroup)
    
    def set_name(self, n):
        self.name = n
        return
    
    def update_time(self):
        self.last_edited = datetime.datetime.now()
        return
          
class Message(models.Model):
    reply_to = models.ForeignKey('self', null=True)
    file = models.ForeignKey(File,null=True)
    web_url = models.URLField(null=True)
    priority_choices = ((1, 'Low'),(2, 'Medium'),( 3, 'High'),)
    priority = models.IntegerField(choices=priority_choices, default=1)
    send_datetime = models.DateTimeField()
    belongs_to_group = models.ForeignKey(JoinInGroup)
    written_by = models.ForeignKey(JoinInUser)
    content = models.CharField(max_length=1000)

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
