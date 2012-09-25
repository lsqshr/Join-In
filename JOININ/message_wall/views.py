# Create your views here.
from django.shortcuts import render_to_response
def hi(request):
    return render_to_response("hi.html")
    