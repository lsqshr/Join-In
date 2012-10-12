'''
Created on 25/09/2012

@author: siqi
'''
from django import forms
from django.forms.widgets import Widget
from django.db.models.fields import CharField

class SignupForm(forms.Form):
    #The user name will be the same as email
    email=forms.EmailField(required=True,label='Your email address:')
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=50,widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,required=True)
    password=forms.CharField(max_length=50,required=True,widget=forms.PasswordInput)
    
class CreateGroupForm(forms.Form):
    name=forms.CharField(max_length=15)
    public=forms.ChoiceField([(True,"Public"),(False,"Private")])
    
class InviteForm(forms.Form):
    username=forms.CharField(max_length=50)