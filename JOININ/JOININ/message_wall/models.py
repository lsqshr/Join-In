from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ManyToManyField
import datetime
from JOININ import accounts.models
          
class Message(models.Model):
    reply_to = models.ForeignKey(Message)
    file_link = models.ForeignKey(File)
    priority = models.IntegerField()
    date_time = models.DateTimeField()
    belongs_to_group = models.ForeignKey(JoinInGroup)
    written_by = models.ForeignKey(JoinInUser)
    content = models.CharField(1000)

    def add_file_link(self, link):
        self.file_link=link
        return
    
    def set_priority(self, p):
        self.priority=p
        return
    
    def set_date_time(self):
        self.date_time=datetime.datetime.now()
        return
    
    def enter_content(self,c):
        self.content=c
        return

class File(models.Model):
    name = models.CharField(20)
    last_edited = models.DateTimeField()
    uploaded_by = models.ForeignKey(JoinInUser)
    belongs_to_group = models.ForeignKey(JoinInGroup)
    
    def set_name(self,n):
        self.name=n
        return
    
    def update_time(self):
        self.last_edited=datetime.datetime.now()
        return

    
    