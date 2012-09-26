# Create your views here.

from JOININ.accounts.forms import SignupForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def login(request):
    return

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