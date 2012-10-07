# Create your views here.
from JOININ.accounts.models import JoinInGroup, JoinInUser
from JOININ.message_wall.forms import SendMessageForm
from JOININ.message_wall.message_wall import MessageWall
from JOININ.message_wall.models import PrivateMessage
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime

def hi(request):
    return render_to_response("base.html")

@login_required
def private_message_wall(request,user_id):
    #get all the groups this person registered
    try:
        user=JoinInUser.objects.get(id=user_id)
    except JoinInUser.DoesNotExist:
        raise "Sorry, this user does not exist. Please contact the system administrator."
    groups=user.groups.all()
    
    if request.method=="POST":
        form=SendMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd.has_key('web_url'):
                web_url=cd['web_url']
            priority=cd['priority']
            if cd.has_key('send_to'):
                send_to=cd['send_to']
            else:
                send_to=None
            belongs_to=cd['belongs_to']
            content=cd['content']
            #get all the entities
            try:
                send_to=JoinInUser.objects.get(user__username=send_to)
            except JoinInUser.DoesNotExist:
                raise "Fail to find the user to send the message. User with email:"+send_to+" does not exist." 
            try:
                belongs_to=JoinInGroup.objects.get(name=belongs_to)
            except JoinInGroup.DoesNotExist:
                raise "Fail to find the group to send the message. Group with name "+belongs_to+" does not exist."
            #send this message
            msgw=MessageWall(owner=user_id)
            msgw.send_message(web_url,send_datetime=datetime.datetime.now(), send_to=send_to, belongs_to=belongs_to, written_by=user, content=content)#did not include priority
             
            #get all the private messages to this user
            p_msgs=msgw.retrieve_list()
            
    else:
        pass 
    #refresh the form to render
    form=SendMessageForm(user_id)
    #add groups to the choicefield of the SendMessageForm
    return render_to_response('message_wall.html',{'form':form,'page_name':'Message Wall', 'private_messages':p_msgs},context_instance=RequestContext(request,{}))
    