"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from JOININ.accounts.models import JoinInUser, JoinInGroup
from JOININ.message_wall.message_wall import *
from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class message_tests(TestCase):
    def send_individual_message_walkthrough(self):
        #get the user to send message
        try:
            user=JoinInUser.objects.get(91)
        except JoinInUser.DoesNotExist:
            raise "user not found"
        #get the group to send the message
        try:
            groups=JoinInGroup.objects.all()
            group=groups[0]
        except JoinInGroup.DoesNotExist:
            raise "group not found"
        #create the message to send
        msgw=MessageWall(user.id)
        msgw.send_message(send_datetime=datetime.datetime.now(),\
                           send_to=user, belongs_to_group=group, \
                           written_by=user, 'hi, I send myself a message!')
        #if the message is send correctly
        msgs=Message.objects.all()
        self.assert_(msgs[0].content=='hi, I send myself a message!', "Message not sent properly")
        p_msgs=PrivateMessage.objects.all()
        self.assert_(p_msgs[0]., )
        #clear the message 