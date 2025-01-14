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
