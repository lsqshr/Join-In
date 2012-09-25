'''
Created on 25/09/2012

@author: siqi
'''

class MessageWall(object):
    '''
    This class is used for keeping the information of 
    messages belonging to user/group, like read/unread.
     MessageList is a temperary list to render on the page.
    '''
    
    class MesageIterator(object):
        '''The iterator for private messages, to assist MessageWall'''
            
        def __init__(self,message_list):
            '''Constructor for MessageIterator'''
            self.message_list=message_list
            
        def retrieve_list(self,type,owner_id,num_of_messages):
            return
        
        def search(self):
            return

    def __init__(self,id):
        '''
        Constructor
        '''
        self._owner_id=id#id of the owner of this class
        self.message_list=[]#the list for private messages
        return
    
    def retrieve_list(self,type,id):
        return
    
    def mark_message_read(self,message_id,is_read):
        return
    
    def mark_priority(self,message_id,priority):
        return
    
    def trash(self,message_id):
        return
    
    def delete_message(self,message_id):
        return
        