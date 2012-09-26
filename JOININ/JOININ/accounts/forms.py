'''
Created on 25/09/2012

@author: siqi
'''
from django import forms

class SignupForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)
    email=forms.EmailField(required=True)
    
    
class LoginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)