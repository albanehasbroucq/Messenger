import requests
import json
from classes_User_Channel_Message import User, Channel, Message
class RemoteServer:

    def __init__(self, url):
        self.url=url

    def get_users(self)-> list[User]:
        response_users=requests.get(self.url+'/users')
        return(User(user[("id")], user["name"]) for user in response_users.json())

    def get_channels(self)-> list[Channel]:
        response_channels=requests.get(self.url+'/channels')
        return(Channel(channel[("id")], channel["name"], channel["member_ids"]) for channel in response_channels.json())
    
    def get_messages(self)-> list[Message]:
        response_messages=requests.get(self.url+'/messages')
        return(Message(mess[("id")], mess["reception_date"], mess["sender_id"], mess["channel"], mess["content"]) for mess in response_messages.json())

    def add_user(self, nom):
        requests.post(self.url+'/users/create', json={"name": nom})

    #def publish_message(self,sender_id, groupe_a_contacter, message_a_ecrire):
    #    requests.post(self.url='users/')

    def add_member_server(self, id_to_add, channel_id):
        requests.post(self.url+f'/channels/{channel_id}/join', json={"user_id": id_to_add})



    def channel_creation(self,name_group,members):
        requests.post(self.url+'/channels/create/', json={"name": name_group})
        for channel in self.get_channels():
            if channel.name == name_group:
                id_group= channel.id
        for member in members:
            self.add_member_server(member,id_group)
    
    def load_server(self):
        return 