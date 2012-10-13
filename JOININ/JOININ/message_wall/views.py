# Create your views here.
from JOININ.accounts.forms import InviteForm, ApplyGroupForm
from JOININ.accounts.models import JoinInGroup, JoinInUser
from JOININ.message_wall.forms import SendMessageForm, FileForm
from JOININ.message_wall.message_wall import MessageWall
from JOININ.message_wall.models import PrivateMessage, JoinInFile
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from django.core.urlresolvers import reverse

@login_required
def private_message_wall(request,link):
    debug=[]
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
        #deal with the form
        if request.method == "POST":
            debug.append("get in deal with form,")
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
                                  send_to=send_to, belongs_to_group=belongs_to, written_by=user, content=content)#did not include priority
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
        return render_to_response('private_message_wall.html', {'form':form,\
                                                                'page_name':'Message Wall', \
                                                                'private_messages':p_msgs,\
                                                                "groups":groups,"debug":debug,'user':request.user.joinin_user},\
                                                                context_instance=RequestContext(request, {}))
    elif link=='apply':
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
                group_to_apply.appliers.add(request.user.joinin_user)
                #TODO:send notification
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
        
@login_required    
def group_message_wall(request, group_id,link):
    #get the group
    group_id = long(group_id)
    group = None
    try:
        group = JoinInGroup.objects.get(id=group_id)
    except:
        raise "Sorry, this group does not exist..." 
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
            if "send" in request.POST:
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
                        except JoinInUser.DoesNotExist:
                            raise Exception("Fail to find the user to send the message. User with email:" + send_to + " does not exist.") 
                        try:
                            belongs_to = JoinInGroup.objects.get(id=belongs_to)
                        except JoinInGroup.DoesNotExist:
                            raise Exception("Fail to find the group to send the message. Group with name " + belongs_to + " does not exist.")
                        #send this message
                        msgw.send_message(web_url=web_url, send_datetime=datetime.datetime.now(),\
                                           send_to=send_to, belongs_to_group=belongs_to,\
                                            written_by=request.user.joinin_user, content=content)#did not include priority
            elif "invite" in request.POST:
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
                        group.users.get(user_username=username)
                        errors.append("Sorry! The user has already been added to this group!")
                    except JoinInGroup.DoesNotExist:
                        pass
                    if errors:
                        return render_to_response("messge_modules/invite_dialog.html",\
                                                  {'errors':errors},context_instance=RequestContext(request, {}))
                    #create new invitation to the user.
                    else:
                        group.invitations.add(user)
        else:
            pass
        #get all the private messages to this user
        p_msgs = msgw.retrieve_list()
        #refresh the form to render
        form = SendMessageForm(user=request.user,initial_group=group)
        #add groups to the choicefield of the SendMessageForm
        #debug bundle
    #    debug=[]
    #    debug.append(user)
    #    debug.append(p_msgs)
        return render_to_response('group_message_wall.html', \
                                  {'form':form, 'page_name':'Message Wall',\
                                    'private_messages':p_msgs, "groups":request.user.joinin_user.groups.all(),\
                                    'users':users,'group':group}, context_instance=RequestContext(request, {}))
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
                        return render_to_response("messge_modules/invite_dialog.html",\
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
        return HttpResponseRedirect("/message_wall/")
    else: 
        return HttpResponse("not working"+link)
    
    
    
# Upload a file and render a list of all files relating to that group
def upload_File(request):
    # UPLOAD
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = JoinInFile(file = request.FILES['file'])
            newfile.save()

            # SETUP LIST
            return HttpResponseRedirect(reverse('JOININ.views.upload_File'))
    else: #There is no file to upload
        form = FileForm()

    # GENERATE LIST
    group_Files = JoinInFile.objects.filter(belongs_to_group='$group_id')

    # RENDERING
    '''
    HANGYU/DANI- Please reference the .html page here
    SIQI- Please check this in urls.py
    return render_to_response(
        'JOININ/xxxxxx  uploadFile.html',
        {'Files for $group_id': group_Files, 'form': form},
        context_instance=RequestContext(request)
    )
    '''