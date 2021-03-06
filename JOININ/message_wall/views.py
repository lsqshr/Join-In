# Create your views here.
from JOININ.accounts.forms import InviteForm, ApplyGroupForm
from JOININ.accounts.models import JoinInGroup, JoinInUser
from JOININ.accounts.views import create_group
from JOININ.message_wall.forms import SendMessageForm
from JOININ.message_wall.message_wall import MessageWall
from JOININ.message_wall.models import Notification, Message, PrivateMessage
from JOININ.message_wall.notification_manager import NotificationManager
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime

@login_required
def private_message_wall(request,link,**kwargs):
    debug=[]
    nm=NotificationManager()
    nm.set_sender(request.user.username, 'smtp.gmail.com', 465, 'lsqshr@gmail.com', '13936344120lsqshr')
    #get all the groups this person registered
    try:
        debug.append("get user\n")
        sys_user = request.user
        #get the joinin user
        user = sys_user.joinin_user
    except JoinInUser.DoesNotExist:
        raise Exception("Sorry, this user does not exist. Please contact the system administrator." \
                        + "USERID:" + str(request.user.id))
    groups = user.groups.all()
    #create the messagewall instance for this view
    msgw = MessageWall(user=user)
    debug.append("ready for the from!")
    if link == 'view':
        #check if notification is set as read
        if kwargs.has_key('notification_id'):
            notification_id=kwargs['notification_id']
            #find the notification and set it as read 
            n=Notification.objects.get(id=notification_id)
            n.is_read=True
            n.save()
        #deal with the form
        if request.method == "POST":
            debug.append("get in deal with form,")
            if 'post_msg'  in request.POST: 
                form = SendMessageForm(request.user,None,request.POST)
                if form.is_valid():
                    debug.append("form valid!")
                    cd = form.cleaned_data
                    if cd.has_key('web_url'):
                        web_url = cd['web_url']
                    priority = cd['priority']
                    if cd.has_key('send_to'):
                        send_to = cd['send_to']
                        if send_to is u'':
                            send_to = None
                    else:
                        send_to = None
                    belongs_to = cd['belongs_to_group']
                    content = cd['content']
                    #get all the entities
                    try:
                        if send_to:
                            send_to = JoinInUser.objects.get(user__username=send_to)
                    except JoinInUser.DoesNotExist:
                        raise Exception("Fail to find the user to send the message. User with email:" + send_to + " does not exist.") 
                    try:
                        belongs_to = JoinInGroup.objects.get(id=belongs_to)
                    except JoinInGroup.DoesNotExist:
                        raise Exception("Fail to find the group to send the message. Group with name " + belongs_to + " does not exist.")
                    #send this message
                    debug.append("ready to send\n")
                    msgw.send_message(web_url=web_url, send_datetime=datetime.datetime.now(), \
                                      send_to=send_to, belongs_to_group=belongs_to, written_by=user, content=content,priority=priority)#did not include priority
                    #send notification to all of the members in that group
                    nm.send_notification(to_user=None, to_group=belongs_to, text=request.user.username+\
                                         " has posted a message in group "+belongs_to.name+".\n\n"\
                                         +str(datetime.datetime.now())+content, \
                                         url="/message_wall/view/", sys=False, email=True)
            elif 'reply' in request.POST:#write reply
                content=request.POST['content']
                message_id=long(request.POST['message_id'])
                group_id=request.POST['group_id']
                #get message to reply to
                try:
                    message=Message.objects.get(id=message_id)
                except Message.DoesNotExist:
                    raise Exception("message not found") 
                try:
                    group=JoinInGroup.objects.get(id=group_id)
                except JoinInGroup.DoesNotExist:
                    raise Exception("group not found")
                Message.objects.create(reply_to=message,priority=1,\
                                       send_datetime=datetime.datetime.now(), \
                                       update_datetime=datetime.datetime.now(),\
                                       belongs_to_group=group,\
                                       written_by=request.user.joinin_user,content=content)
                #change the parent message's update_datetime for sorting
                message.update_datetime=datetime.datetime.now() 
                message.save()
                return HttpResponseRedirect('/message_wall/view/')
            elif 'apply' in request.POST:
                #deal with the form
                if request.method == 'POST':
                    form=ApplyGroupForm(request.POST)
                    errors=[]
                    if form.is_valid():
                        cd=form.cleaned_data
                        group_name=cd['group_name']
                        #find the group
                        group_to_apply=None
                        try:
                            group_to_apply=JoinInGroup.objects.get(name=group_name)
                        except JoinInGroup.DoesNotExist:
                            errors.append("Sorry, group with name<b>"+group_name+"</b> does not exist, please check the name.")
                        #add the user to the appliers of that group
                        if request.user.joinin_user not in group_to_apply.appliers.all() or \
                                request.user.joinin_user not in group_to_apply.users.all():
                            group_to_apply.appliers.add(request.user.joinin_user)
                            
                        else:#TODO:
                            raise "You have applied for this group or you have been a member of this group. Please be patient for the acceptance."
                        #send notification
                        nm.send_notification(request.user.joinin_user, None, 'You have applied to join group '+group_to_apply.name\
                                             +'.Please wait for permission. Any of the members in this group are able to allow you to join in.', None) 
                        #redirect to the private message wall
                        return HttpResponseRedirect("/message_wall/view/")
                    else:#group name is not in the right format
                        errors.append("OOps!The group name is too long...")
                    if errors:    
                        return render_to_response("accounts_modules/apply_dialog.html",{'form':form,'errors':errors},\
                                          context_instance=RequestContext(request, {}))       
                    else:
                        form=ApplyGroupForm()
                    #show the apply group dialog
                    return render_to_response("accounts_modules/apply_dialog.html",{'form':form},\
                                              context_instance=RequestContext(request, {}))
            elif 'create_group' in request.POST:
                return create_group(request)
        else:
            pass
        #get all the private messages to this user
        p_msgs = msgw.retrieve_list()
        #refresh the form to render
        form = SendMessageForm(user=request.user)
        #add groups to the choicefield of the SendMessageForm
        #debug bundle
    #    debug=[]
    #    debug.append(user)
    #    debug.append(p_msgs)
        #get notifications
        if kwargs.has_key('see') and kwargs['see'] == 'all_notifications':
            notifications=nm.get_all_notification(user)
            see_all_notifications=True
        elif kwargs.has_key('see') and kwargs['see']=='unread_notifications' \
                or not kwargs.has_key('see'):
            notifications=nm.get_unread_notification(user)
            see_all_notifications=False
        return render_to_response('private_message_wall.html', {'form':form,\
                                                                'page_name':'Hi, '+user.user.username,\
                                                                'page_tag':'private',\
                                                                'private_messages':p_msgs,\
                                                                "groups":groups,'notifications':notifications,\
                                                                'see_all_notifications':see_all_notifications,\
                                                                "debug":debug,'user':request.user.joinin_user},\
                                                                context_instance=RequestContext(request, {}))
    #elif link=='apply':
        
    elif link == 'accept':#accept one groupe's invitation 
        #get groupto accept invitation
        group_id=long(kwargs['group_id'])
        try:
            group_to_join=JoinInGroup.objects.get(id=group_id)
        except JoinInGroup.DoesNotExist:
            #TODO:
            raise Exception("Sorry, This group does not exist any more.")
        #add this user to that group
        if request.user.joinin_user in group_to_join.invitations.all() and \
                request.user.joinin_user not in group_to_join.users.all():
            group_to_join.users.add(request.user.joinin_user)
            for msg in group_to_join.messages.all():
                PrivateMessage.objects.create(message=msg, belongs_to=request.user.joinin_user, read=False, priority=msg.priority, trashed=False)
        #delete the invitation
        group_to_join.invitations.remove(request.user.joinin_user)
        #TODO:send notification to this user
        nm.send_notification(request.user.joinin_user,None, \
                             "Congratulations, you are now in group "+group_to_join.name+'.',\
                              '/message_wall/group/'+str(group_to_join.id)+'/view/')
        return HttpResponseRedirect('/message_wall/view/')
    elif link == 'deny':
        #get groupto accept invitation
        group_id=long(kwargs['group_id'])
        try:
            group_to_join=JoinInGroup.objects.get(id=group_id)
        except JoinInGroup.DoesNotExist:
            #TODO:
            raise Exception("Sorry, This group does not exist any more.")
        #simply remove the user from the invitations
        group_to_join.invitations.remove(request.user.joinin_user)
        return HttpResponseRedirect('/message_wall/view/')           
    
@login_required    
def group_message_wall(request, group_id,link,**kwargs):
    nm=NotificationManager()
    nm.set_sender(request.user.username, 'smtp.gmail.com', 465, 'lsqshr@gmail.com', '13936344120lsqshr')
    #get the group
    group_id = long(group_id)
    group = None
    try:
        group = JoinInGroup.objects.get(id=group_id)
    except:
        raise Exception("Sorry, this group does not exist..." )
    #see if this user has permission to view the group content
    try:
        group.users.get(user__username=request.user.username)
    except JoinInUser.DoesNotExist:
        return HttpResponse("sorry, you do not have the permission to view this group. Group Name:"\
                            +str(group.name)+"Your user id:"+str(request.user.id))
    if link == 'view':#deal with when the url is like /group_id/view/
        #
        #get all the messages to render
        messages=group.messages.all()
        #get all the members
        users=group.users.all()
        msgw=MessageWall(user=request.user.joinin_user,group=group)
        #TODO: get all the files
        ####################deal with form#########################################
        if request.method == "POST":
            if "post_msg" in request.POST:
                    form = SendMessageForm(request.user,group, request.POST)
                    if form.is_valid():
                        cd = form.cleaned_data
                        if cd.has_key('web_url'):
                            web_url = cd['web_url']
                        priority = cd['priority']
                        if cd.has_key('send_to'):
                            send_to = cd['send_to']
                            if send_to is u'':
                                send_to = None
                        else:
                            send_to = None
                        belongs_to = cd['belongs_to_group']
                        content = cd['content']
                        #get all the entities
                        try:
                            if send_to:
                                send_to = JoinInUser.objects.get(user__username=send_to)
                        except JoinInUser.DoesNotExist:#TODO:
                            raise Exception("Fail to find the user to send the message. User with email:" + send_to + " does not exist.") 
                        try:
                            belongs_to = JoinInGroup.objects.get(id=belongs_to)
                        except JoinInGroup.DoesNotExist:
                            raise Exception("Fail to find the group to send the message. Group with name " + belongs_to + " does not exist.")
                        #send this message
                        msgw.send_message(web_url=web_url, send_datetime=datetime.datetime.now(),\
                                           send_to=send_to, belongs_to_group=belongs_to,\
                                            written_by=request.user.joinin_user, content=content,priority=priority)#did not include priority
                        #send notification to all of the members in that group
                        nm.send_notification(to_user=None, to_group=belongs_to, text=request.user.username+\
                                             " has posted a message in group "+belongs_to.name+".\n\n"\
                                             +str(datetime.datetime.now())+content, \
                                             url="/message_wall/view/", sys=False, email=True)
            elif "invite" in request.POST:#deal with the 
                form=InviteForm(request.POST)
                if form.is_valid():
                    cd=form.cleaned_data
                    username=cd['username']
                    #get the user
                    errors=[]
                    try:
                        user=JoinInUser.objects.get(user__username=username)
                    except JoinInUser.DoesNotExist:
                        #show the form again.
                        errors.append("Sorry! The user does not exist.")
                    #see if the user is in the group now    
                    try:
                        group.users.get(user__username=username)
                        errors.append("Sorry! The user has already been added to this group!")
                    except JoinInUser.DoesNotExist:
                        pass
                    if errors:
                        NotificationManager().send_notification(request.user.joinin_user, None, ';'.join(errors), None, True,False)
                        return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
                    #create new invitation to the user.
                    else:
                        group.invitations.add(user)
                        return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
            elif 'reply' in request.POST:#write reply
                content=request.POST['content']
                message_id=long(request.POST['message_id'])
                group_id=request.POST['group_id']
                #get message to reply to
                try:
                    message=Message.objects.get(id=message_id)
                except Message.DoesNotExist:
                    raise Exception("message not found") 
                try:
                    group=JoinInGroup.objects.get(id=group_id)
                except JoinInGroup.DoesNotExist:
                    raise Exception("group not found")
                Message.objects.create(reply_to=message,priority=1,\
                                       send_datetime=datetime.datetime.now(), \
                                       update_datetime=datetime.datetime.now(),\
                                       belongs_to_group=group,\
                                       written_by=request.user.joinin_user,content=content)
                #change the parent message's update_datetime for sorting
                message.update_datetime=datetime.datetime.now() 
                message.save()
                return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
            elif 'apply' in request.POST:
                #deal with the form
                if request.method == 'POST':
                    form=ApplyGroupForm(request.POST)
                    errors=[]
                    if form.is_valid():
                        cd=form.cleaned_data
                        group_name=cd['group_name']
                        #find the group
                        group_to_apply=None
                        try:
                            group_to_apply=JoinInGroup.objects.get(name=group_name)
                        except JoinInGroup.DoesNotExist:
                            errors.append("Sorry, group with name<b>"+group_name+"</b> does not exist, please check the name.")
                        #add the user to the appliers of that group
                        if request.user.joinin_user not in group_to_apply.appliers.all() or \
                                request.user.joinin_user not in group_to_apply.users.all():
                            group_to_apply.appliers.add(request.user.joinin_user)
                        else:#TODO:
                            raise "You have applied for this group or you have been a member of this group. Please be patient for the acceptance."
                        #send notification
                        nm.send_notification(request.user.joinin_user, None, 'You have applied to join group '+group_to_apply.name\
                                             +'.Please wait for permission. Any of the members in this group are able to allow you to join in.', None) 
                        #redirect to the private message wall
                        return HttpResponseRedirect("/message_wall/view/")
                    else:#group name is not in the right format
                        errors.append("OOps!The group name is too long...")
                    if errors:    
                        return render_to_response("accounts_modules/apply_dialog.html",{'form':form,'errors':errors},\
                                          context_instance=RequestContext(request, {}))       
                    else:
                        form=ApplyGroupForm()
                    #show the apply group dialog
                    return render_to_response("accounts_modules/apply_dialog.html",{'form':form},\
                                              context_instance=RequestContext(request, {}))
        else:
            pass
        #get all the private messages to this user
        p_msgs = msgw.retrieve_list()
        #refresh the form to render
        form = SendMessageForm(user=request.user,initial_group=group)
        #get applisers to this group
        appliers=group.appliers.all()
        return render_to_response('group_message_wall.html', \
                                  {'form':form, 'page_name':'Group '+group.name+' Message Wall',\
                                    'page_tag':'public',\
                                    'private_messages':p_msgs, "groups":request.user.joinin_user.groups.all(),\
                                    'users':users,'group':group,'appliers':appliers},\
                                   context_instance=RequestContext(request, {}))
    elif link == 'invite':
        if request.method=="POST"and "invite" in request.POST:
                form=InviteForm(request.POST)
                if form.is_valid():
                    cd=form.cleaned_data
                    username=cd['username']
                    #get the user
                    errors=[]
                    try:
                        user=JoinInUser.objects.get(user__username=username)
                    except JoinInUser.DoesNotExist:
                        #show the form again.
                        errors.append("Sorry! The user does not exist.")
                    #see if the user is in the group now    
                    try:
                        group.users.get(user__username=username)
                        errors.append("Sorry! The user has already been added to this group!")
                    except JoinInUser.DoesNotExist:
                        pass
                    if errors:
                        return render_to_response("accounts_modules/invite_dialog.html",\
                                                  {'errors':errors,'form':form,'group':group},\
                                                   context_instance=RequestContext(request, {}))
                    #create new invitation to the user.
                    else:
                        group.invitations.add(user)
                        #TODO:should send user a notification to notify success of inviting the user.
                        return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
        else:#no submit form
            form=InviteForm() 
            return render_to_response("accounts_modules/invite_dialog.html",\
                                      {'group':group,'form':form},\
                                       context_instance=RequestContext(request, {}))
    elif link == 'leave':
        #delete the current user from this group
        group.users.remove(request.user.joinin_user)
        #TODO:send notification to notify user that the user has left the group
        #redirect to the private message wall
        #if the group has no more user, this group should be deleted
        if len(group.users.all()) is 0:
            group.delete()
        return HttpResponseRedirect("/message_wall/view/")
    elif link == 'accept':
        #get user
        try:
            user_to_add= JoinInUser.objects.get(user__username=kwargs['username'])
        except JoinInUser.DoesNotExist:
            raise "User Does not exist!"#TODO:
        #see if this user is in the group, not? add!
        if user_to_add not in group.users.all()\
                and len(group.users.all())<=12:
            group.users.add(user_to_add) 
        else:
            NotificationManager().send_notification(request.user.joinin_user, None, 'User '+user_to_add.user.username+\
                                                    ' has already been in the group. Or there are already 12 members in this group, which reached the top limit.',\
                                                     None,True,False)
        #delete this user from appliers
        group.appliers.remove(user_to_add)
        #delete the user from the invitations, if there are invitation was sent to this user
        if user_to_add in group.invitations.all():
            group.invitations.remove(user_to_add)
        #send all the messages in that group as private messages to the user,
        #since the new user should see the historical messages
        for msg in group.messages.all():
            PrivateMessage.objects.create(message=msg, belongs_to=user_to_add, read=False, priority=msg.priority, trashed=False)
        
        #redirect
        return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
    elif link== 'deny':
        #get user 
        #get user
        try:
            user_to_add= JoinInUser.objects.get(user__username=kwargs['username'])
        except JoinInUser.DoesNotExist:
            raise "User Does not exist!"#TODO:
        #simply remove this joinin user from the appliers
        group.appliers.remove(user_to_add)
        return HttpResponseRedirect('/message_wall/group/'+str(group.id)+'/view/')
    else: 
        return HttpResponse("not working"+link)

def mark_read(request,**kwargs):
    msg_id=kwargs['message_id']
    msg_id=long(msg_id)
    try:
        pmsg=PrivateMessage.objects.get(id=msg_id)
    except:
        raise Exception("message not found.")
    if kwargs['mark'] == 'mark_as_read':
        pmsg.read=True
        pmsg.save()
    else:
        pmsg.read=False
        pmsg.save()
    if kwargs.has_key('group_id'):
        group_id=kwargs['group_id']
        group_id=str(group_id)
        return HttpResponseRedirect('/message_wall/group/'+group_id+'/view/')
    else:
        return HttpResponseRedirect('/message_wall/view/')

