import requests
import json
from classes_User_Channel_Message import User, Channel, Message

class Server:
    def __init__(self, url):
        pass

    def get_users(self)-> list[User]:
        pass

    def get_channels(self)-> list[Channel]:
        pass
    
    def get_messages(self)-> list[Message]:
        pass

    def add_user(self, nom):
        pass

    def publish_message(self,sender_id, groupe_a_contacter, message_a_ecrire):
        pass

    def add_member_server(self, id_to_add, channel_id):
        pass

    def channel_creation(self,name_group,members):
        pass
