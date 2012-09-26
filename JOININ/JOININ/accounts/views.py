from JOININ.accounts.forms import SignupForm, LoginForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username=cd['username']
            password=cd['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                #Correct Password, and User is marked "active"
                auth.login(request,user)
                #Redirect to a success page.
                return HttpResponseRedirect("/message_wall/"+str(user.id)+'/')
            else:
                return render_to_response('login.html',{'form':form},context_instance=RequestContext(request,{}))
    else:
        form=LoginForm()
    return render_to_response('login.html',{'form':form},context_instance=RequestContext(request,{}))


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user=User.objects.create_user(cd['username'],cd['email'],cd['password'])
            #redirect to the congratulations view
            return HttpResponseRedirect('/congratulation_for_signup/')
    else:
        form=SignupForm()
    return render_to_response('signup.html',{'form':form},context_instance=RequestContext(request,{}))


def congrats(request):
    return render_to_response("congrats_signup.html")