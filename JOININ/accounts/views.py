from JOININ.accounts.forms import SignupForm, LoginForm, CreateGroupForm, \
    SettingsForm
from JOININ.accounts.models import JoinInUser, JoinInGroup
from JOININ.message_wall.notification_manager import NotificationManager
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime

def login(request):
    errors=[]
    if request.method == "POST":
        if 'login_submit' in request.POST:#user submited the form to login
            form = LoginForm(request.POST)
            register_form=SignupForm()
            if form.is_valid():
                cd = form.cleaned_data
                username=cd['username']
                password=cd['password']
                user=auth.authenticate(username=username,password=password)
                if user is not None and user.is_active:
                    #Correct Password, and User is marked "active"
                    auth.login(request, user)
                    #Redirect to a success page.
                    return HttpResponseRedirect("/message_wall/view/") 
                else:
                    errors.append('Your username or password is incorrect,please try again.')
                    return render_to_response('login.html',{'login_form':form,\
                                                            'register_form':register_form,\
                                                            'page_name':'Log-in','errors':errors},\
                                                            context_instance=RequestContext(request,{}))
            else:# form is not valid
                errors.append('Please provide valid username and password to access this system.')
                return render_to_response('login.html',{'login_form':form,\
                                                            'register_form':register_form,\
                                                            'page_name':'Log-in','errors':errors},\
                                                            context_instance=RequestContext(request,{}))
        else:#user submit the register form
            register_form = SignupForm(request.POST)
            if register_form.is_valid():
                cd = register_form.cleaned_data
                email = cd['email']
                password = cd['password']
                confirm_password = cd['confirm_password']
                errors = []#errors list to be rendered
                #see if two password match each other
                if password != confirm_password:
                    errors.append('Sorry, two password do not match each other.')
                #see if the same email has been registered
                try:
                        User.objects.get(username=email)
                        errors.append('Sorry,this email address has been used,please change another one')
                except:
                        pass         
                if errors:
                    return render_to_response('login.html', {'register_form':register_form,
                                                              'login_form':LoginForm(), 'errors':errors},
                                                               context_instance=RequestContext(request, {}))
                new_joinin_user = JoinInUser.objects.create_user(email, password)
                user=auth.authenticate(username=email,password=password)
                if user is not None and user.is_active:
                    #Correct Password, and User is marked "active"
                    auth.login(request, user)
                    #Redirect to a success page.
                    #redirect to the congratulations view
                    return render_to_response('congrats_signup.html', {'user':new_joinin_user.user})
            else:
                errors.append('Please provide valid username and password to access this system.')
                return render_to_response('login.html',{'login_form':LoginForm(),\
                                                            'register_form':register_form,\
                                                            'page_name':'Log-in',\
                                                            'errors':register_form.errors},\
                                                            context_instance=RequestContext(request,{}))
    else:
        login_form = LoginForm()
        register_form=SignupForm()
    return render_to_response('login.html', {'register_form':register_form,'login_form':login_form,'page_name':'Log-in'}, context_instance=RequestContext(request, {}))



def forget_password(request):
    return HttpResponse("forget!");

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

@login_required
def create_group(request):
    #get the current user
    user = request.user.joinin_user
    errors=[]
    #get data from the form
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            public = cd['public']
            #create new JoinInGroup
            group_exist=False
            try:#see if the group name has been created before
                JoinInGroup.objects.get(name=name)
                group_exist=True
            except JoinInGroup.DoesNotExist:
                group_exist=False
            if(not group_exist):
                new_group = JoinInGroup.objects.create(name=name, create_datetime=datetime.datetime.now(), \
                                                 public=public, creator=user)
                new_group.users.add(user)
                #TODO:send notification
                NotificationManager().send_notification(request.user.joinin_user, None, "You have successfull created a group called"\
                                                        +name+". You can go to the your own group page and invite other users by their emails.", None, True, False)
                return HttpResponseRedirect('/message_wall/view/')
            else:
                errors.append("The group name "+name+" has been taken. Please choose another one.")
                #TODO:send notification
                NotificationManager().send_notification(request.user.joinin_user, None,'; '.join(errors), None, True, False)
        else:
            raise Exception("form not valid")         
    return HttpResponseRedirect('/message_wall/view/')

def settings(request):
    errors=[]
    if request.method == "POST" and 'settings' in request.POST:
        form=SettingsForm(request.POST,instance=request.user.joinin_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/message_wall/view/')
        else:
            errors=form.errors
    else:
        form=SettingsForm(instance=request.user.joinin_user) 
    return render_to_response("settings.html",{'form':form,'errors':errors},context_instance=RequestContext(request, {}))
        
