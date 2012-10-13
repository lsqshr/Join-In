'''
Created on 07/10/2012

@author: siqi
'''
from django import forms
from django.forms.widgets import Textarea


class SendMessageForm(forms.Form):
    web_url=forms.URLField(required=False,label='web_url:')
    priority=forms.ChoiceField([(2,"Just message"),(1,"Ignore me"),(3,"Urgent")],label='priority:')
    send_to=forms.CharField(max_length=50,required=False,label='send_to:',help_text='The email of the receiver. Blank means the whole group.')
    content=forms.CharField(max_length=140,widget=Textarea,help_text='your message here.')
    belongs_to_group=forms.ChoiceField()

    #TODO: files upload needed
    
    #override the constructor of form
    def __init__(self,user,initial_group=None,*args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        #get groups
        self.initial['priority']=2
        groups=user.joinin_user.groups.all()
        choices=[ (o.id, o.name) for o in groups]
        self.fields['belongs_to_group']=forms.ChoiceField(choices,label='to group:')#this part is dynamic, need to find the groups that this user has registered
        if initial_group:
            self.initial['belongs_to_group']=initial_group.id
            
class FileForm(forms.Form):
    file = forms.FileField(
        label='Select File for Upload'
    )
