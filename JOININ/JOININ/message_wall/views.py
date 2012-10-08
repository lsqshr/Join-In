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
        sys_user=request.user
        #get the joinin user
        user=sys_user.joinin_user
    except JoinInUser.DoesNotExist:
        raise Exception("Sorry, this user does not exist. Please contact the system administrator."+"USERID:"+str(user_id))
    groups=user.groups.all()
    #create the messagewall instance for this view
    msgw=MessageWall(user=user)
    #deal with the form
    if request.method=="POST":
        form=SendMessageForm(request.user,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd.has_key('web_url'):
                web_url=cd['web_url']
            priority=cd['priority']
            if cd.has_key('send_to'):
                send_to=cd['send_to']
            else:
                send_to=None
            belongs_to=cd['belongs_to_group']
            content=cd['content']
            #get all the entities
            try:
                send_to=JoinInUser.objects.get(user__username=send_to)
            except JoinInUser.DoesNotExist:
                raise Exception("Fail to find the user to send the message. User with email:"+send_to+" does not exist.") 
            try:
                belongs_to=JoinInGroup.objects.get(id=belongs_to)
            except JoinInGroup.DoesNotExist:
                raise Exception("Fail to find the group to send the message. Group with name "+belongs_to+" does not exist.")
            #send this message
            msgw.send_message(web_url=web_url,send_datetime=datetime.datetime.now(), send_to=send_to, belongs_to_group=belongs_to, written_by=user, content=content)#did not include priority
    else:
        pass 
    #get all the private messages to this user
    p_msgs=msgw.retrieve_list()
    #refresh the form to render
    form=SendMessageForm(user=request.user)
    #add groups to the choicefield of the SendMessageForm
    #debug bundle
#    debug=[]
#    debug.append(user)
#    debug.append(p_msgs)
    return render_to_response('message_wall.html',{'form':form,'page_name':'Message Wall', 'private_messages':p_msgs},context_instance=RequestContext(request,{}))
    