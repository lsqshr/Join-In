"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from JOININ.accounts.models import JoinInUser, JoinInGroup
from JOININ.message_wall.message_wall import *
from django.db.models import Q
from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 1)

class message_tests(TestCase):
    def send_individual_message_walkthrough(self):
        #get the user to send message
        try:
            user=JoinInUser.objects.get(user__username='lsqshr')
        except JoinInUser.DoesNotExist:
            raise "user not found"
        #get the group to send the message
        try:
            group=JoinInGroup.objects.get(name='testgroup')
        except JoinInGroup.DoesNotExist:
            raise "group not found"
        #create the message to send
        msgw=MessageWall(user.id)
        msg=msgw.send_message(send_datetime=datetime.datetime.now(),\
                           send_to=user, belongs_to_group=group, \
                           written_by=user, content='hi, I send myself a message!')
        #if the message is send correctly
        #find the message
        msg_in_db=Message.objects.get(id=msg.id)
        self.assertEqual(msg_in_db.content,msg.content,'individual message not sent properly!')
        p_msg=msg_in_db.private_messages.get(message__id=msg_in_db.id)        
        self.assertNotEqual(p_msg.message.send_to,user,"individual Private message not sent properly!" )
        
        #clear the message
        for pmsg in msg.private_messages:
            pmsg.delelte()
        msg.delete()
        return
    
    def send_group_message_walkthrough(self):
        #get the user to send message
        try:
            user=JoinInUser.objects.get(user__username='lsqshr')
        except JoinInUser.DoesNotExist:
            raise "user not found"
        #get the group to send the message
        try:
            group=JoinInGroup.objects.get(name='testgroup')
        except JoinInGroup.DoesNotExist:
            raise "group not found"
        #create the message to send
        msgw=MessageWall(user.id)
        msg=msgw.send_message(send_datetime=datetime.datetime.now(),\
                           send_to=None, belongs_to_group=group, \
                           written_by=user, content='hi, I send my group a message!')
        #if the message is send correctly
        #find the message
        msg_in_db=Message.objects.get(id=msg.id)
        self.assertEqual(msg_in_db.content,msg.content,'group message not sent properly')
        p_msg=msg_in_db.private_messages.get(Q(message__id=msg_in_db.id),Q(belongs_to__id=user.id))        
        self.assertEqual(p_msg.message.id , msg_in_db.id,"individual Private message not sent properly!")
        
        #clear the message
        for pmsg in msg.private_messages:
            pmsg.delelte()
        msg.delete()
        return 
    
'''
group=JoinInGroup.objects.create()
#see if many to many works
print "joinin groups:"
groups=JoinInGroup.objects.all()
group=groups[0]
invitations=group.invitations.all()
for user in invitations:
    print user
applers=group.appliers.all()
for user in invitations:
    print user

'''