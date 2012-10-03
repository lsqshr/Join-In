from JOININ.accounts.forms import SignupForm, LoginForm
from JOININ.accounts.models import JoinInUser
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
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
                return render_to_response('login.html',{'form':form,'page_name':'Log-in'},context_instance=RequestContext(request,{}))
    else:
        form=LoginForm()
    return render_to_response('login.html',{'form':form,'page_name':'Log-in'},context_instance=RequestContext(request,{}))


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email=cd['email']
            password=cd['password']
            confirm_password=cd['confirm_password']
            errors=[]#errors list to be rendered
            #see if two password match each other
            if password!=confirm_password:
                errors.append('Sorry, two password do not match each other.')
               
            #see if the same email has been registered
            try:
                    User.objects.get(username=email)
                    errors.append('Sorry,this email address has been used,please change another one')
            except:
                    pass         
            if errors:
                return render_to_response('signup.html',{'form':form,'errors':errors,'page_name':'Register'},context_instance=RequestContext(request,{}))
            new_joinin_user=JoinInUser.objects.create_user(email, password)
            #redirect to the congratulations view
            return render_to_response('congrats_signup.html',{'user':new_joinin_user.user}) 
    else:
        form=SignupForm()
    return render_to_response('signup.html',{'form':form,'page_name':'Register'},context_instance=RequestContext(request,{}))

def forget_password(request):
    return HttpResponse("forget!");