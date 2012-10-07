'''
Created on 25/09/2012

@author: siqi
'''
from JOININ.message_wall.models import *

class MessageWall(object):
    '''
    This class is used for keeping the information of 
    messages belonging to user/group, like read/unread.
     MessageList is a temperary list to render on the page.
    '''
    
    class MessageIterator(object):
        '''The iterator for private messages, to assist MessageWall'''
            
        def __init__(self):
            '''Constructor for MessageIterator'''
            self.message_list = None
        def retrieve_list(self, type, owner_id, group_id, start=None, end=None):
            #TODO:add limit to the retrieve record number. start to end, use [:] to slice the result set
            self.message_list = PrivateMessage.get_messages(self._owner_id, self._group_id)#the list for private messages
            return self.message_list
        
        def search(self):
            return
        
        def get_list(self):
            return self.message_list

    def __init__(self, user_id, group_id=None):
        '''
        Constructor
        @param id: id of user/group
        @param is_group: whether this class's owner is a group  
        '''
        self._owner_id = user_id#id of the owner of this class
        self._group_id = group_id
        self.msg_iter = self.MessageIterator()
        return
    
    def retrieve_list(self, start=None, end=None):
        #currently it just retrieve all the message relevant to this user once this method is called
        #In the future, we will take the memory efficiency into consideration.
        
        return self.msg_iter.retrieve_list(None, self.owner_id, self.group_id, start, end)
    
    def mark_message_read(self, message_id, is_read):
        #get the private_message matching the message_id
        try:
            p_msg = PrivateMessage.objects.get(message__id=message_id)
            p_msg.read = is_read
            p_msg.save()
        except PrivateMessage.DoesNotExist:
            raise 'Error. The message not found.'
        return
    
    def mark_priority(self, message_id, priority):
        #get the private_message matching the message_id
        try:
            p_msg = PrivateMessage.objects.get(message__id=message_id)
            p_msg.priority = priority
            p_msg.save()
        except PrivateMessage.DoesNotExist:
            raise 'Error. The message not found.' 
        return
    
    def trash(self, message_id):
        #get the private_message matching the message_id
        try:
            p_msg = PrivateMessage.objects.get(message__id=message_id)
            p_msg.trashed = True
            p_msg.save()
        except PrivateMessage.DoesNotExist:
            raise 'Error. The message not found.' 
        return
    
    def delete_message(self, message_id):
        #get the private_message matching the message_id
        try:
            PrivateMessage.objects.get(message__id=message_id).delete()
        except PrivateMessage.DoesNotExist:
            raise 'Error. The message not found.' 
        return
        
    def send_message(self, reply_to=None, web_url=None, priority=2, \
                      send_datetime=None, send_to=None, belongs_to_group=None,\
                       written_by=None, content=None, files=None):
        #files should be a list of file models
        #@param send_to: if send_to is not setted, it means this message is going 
        #to be send to the whole group stated 
        #create a new message,if send_to is None, then send this message to the whole group
        msg = Message.objects.create(reply_to, web_url, priority,\
                                      send_datetime, send_to, belongs_to_group, written_by, content);
        #create files
        for file in files:
            file.message = msg
            file.save()
        #find the group this message is expected to be sent to
        try:
                group = JoinInGroup.objects.get(id=belongs_to_group)
        except JoinInGroup.DoesNotExist:
                raise "Group not found"
        #create private messages relevant to where this message is expected to be sent
        if send_to is None:
           
            #find the users in that group
            users = group.joinin_users
            #for each user in that group, create a new private message
            for user in users:
                p_msg = PrivateMessage.objects.create(msg, user, False, 2, False)
                p_msg.save()
        else: 
            p_msg = PrivateMessage.objects.create(msg, send_to, False, 2, False) 
        return msg
