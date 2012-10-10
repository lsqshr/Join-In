'''
Created on 07/10/2012

@author: siqi
'''
from django import forms

class SendMessageForm(forms.Form):
    web_url=forms.URLField(required=False)
    priority=forms.ChoiceField([(2,"Just message"),(1,"Ignore me"),(3,"Urgent")])
    send_to=forms.CharField(max_length=50,required=False)
    content=forms.CharField(max_length=140)
    belongs_to_group=forms.ChoiceField()
    #TODO: files upload needed
    
    #override the constructor of form
    def __init__(self,user,initial_group=None,*args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        #get groups
        groups=user.joinin_user.groups.all()
        choices=[ (o.id, o.name) for o in groups]
        self.fields['belongs_to_group']=forms.ChoiceField(choices)#this part is dynamic, need to find the groups that this user has registered
        if initial_group:
            self.fields['belongs_to_group'].initial=initial_group
