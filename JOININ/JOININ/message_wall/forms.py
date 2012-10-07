'''
Created on 07/10/2012

@author: siqi
'''
from django import forms

class SendMessageForm(forms.Form):
    web_url=forms.URLField(required=False)
    priority=forms.IntegerField()
    send_to=forms.CharField(max_length=50,required=False)
    belongs_to_group=forms.ChoiceField()#this part is dynamic, need to find the groups that this user has registered
    #need to be set manually by the message wall view, before this form is going to be sent.
    content=forms.CharField(max_length=140)
    #TODO: files upload needed
    
    #constructor
    def __init__(self,user,*args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)

        #get groups
        groups=user.joinin_user.groups.all()
        self.choices=[ (o.id, str(o.name)) for o in groups]
        self.belongs_to_group=forms.ChoiceField(self.choices)#this part is dynamic, need to find the groups that this user has registered
