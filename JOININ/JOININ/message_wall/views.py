# Create your views here.
from django.shortcuts import render_to_response
def hi(request):
    return render_to_response("base.html")

def private_message_wall(request,user_id):
    return render_to_response('hi.html')
    