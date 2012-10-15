'''
Created on 15/10/2012

@author: siqi
'''
from JOININ import settings
from JOININ.message_wall.models import Notification
from django.core.mail.message import EmailMessage
import datetime

class NotificationManager(object):
    
    '''
    This class is designed to aggregate the functions to be 
    used for sending(including emailling) and gathering notifications.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.from_email=None
        self.is_sender_set=False
        pass
    
    def send_notification(self, to_user=None, to_group=None, text=None, url=None):
        if to_user.system_notification:#check if the user allow the system to send system notification
            self._send_sys_notification(to_user, text, url)
        if to_user.email_update:
            self._send_email_notification(to_user.user.username, text, url)
        return
    
    def _send_email_notification(self, email, text, url):
        '''
        Note: To use this method, should call set_send() first!
        '''
        if self.is_sender_set:
            em = EmailMessage(subject="JoinIn Notification",\
                            body=text, from_email=self.from_email, to=[email],)
            em.send(fail_silently=False) 
        else:
            raise Exception("Sender not set!")
        return
    
    def _send_sys_notification(self, to_user, text, url):
        '''
        simply create a notification instance for that user
        '''
        Notification.objects.create(user=to_user, \
                                    content=text, url=url, send_datetime=datetime.datetime.now())
        return
    
    def get_unread_notification(self, user):
        return Notification.objects.filter(user=user,is_read=False).order_by('send_datetime')
    
    def set_sender(self,sender_email,smtp_host,smtp_port,username,password):
        #better design with smtp servers stored in the database end
            self.email=sender_email
            settings.EMAIL_HOST = smtp_host
            settings.EMAIL_PORT = smtp_port
            settings.EMAIL_HOST_USER = username
            settings.EMAIL_HOST_PASSWORD = password
            self.is_sender_set=True
            return 