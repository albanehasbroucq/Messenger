from classes_User_Channel_Message import User, Channel, Message
import json
from typing import override
from class_Server import Server

class LocalServer (Server):

    @override
    def __init__(self, nom_fichier: str):
        self.nom_fichier = nom_fichier
        self.users: list[User]=[]
        self.channels: list[Channel]=[]
        self.messages: list[Message]=[]

        self.load_server()
        
    # def __init__(self, users: list[User], channels: list[Channel], messages: list[Message]):
    #     self.users=users
    #     self.channels=channels
    #     self.messages=messages
    
    @override
    def __repr__(self) -> str:
        return f'Server(users={self.users}, channels={self.channels})'
    
    @override
    def load_server(self):
        with open(self.nom_fichier) as json_file:
            server=json.load(json_file)

            users = [User(user['id'], user['name']) for user in server['users']]
            self.users = users

            channels = [Channel(channel['id'], channel['name'], channel['member_ids'])for channel in server['channels']]
            self.channels = channels

            messages = [Message(mess['id'], mess['reception_date'], mess['sender_id'], mess['channel'], mess['content']) for mess in server['messages']]
            self.messages = messages
        ## server['users']:list[dict]
        ## Transform server['users'] en list[User]

        return server
    #with open('server-data.json', 'r') as fichier:
    #    server = json.load(fichier)
    @override
    def save_server(self):
        dic={}
        dic['users'] = [user.to_dict() for user in self.users]
        dic['channels'] = [channel.to_dict() for channel in self.channels]
        dic['messages'] = [mess.to_dict() for mess in self.messages]
        with open(self.nom_fichier, 'w') as fichier:
            json.dump(dic, fichier)
            #json.dump(dic, fichier, indent=4, ensure_ascii=False)

    @override
    def get_users(self)->list[User]:
        return(self.users)
    
    @override
    def get_channels(self)->list[Channel]:
        return(self.channels)
    
    @override
    def get_messages(self)->list[Message]:
        return(self.messages)
    #def add_message(self, message:Message):

    @override
    def add_user(self, nom):
        n_id = max([u.id for u in self.get_users()])+1
        self.get_users().append(User(n_id,nom))
        self.save_server()

    @override
    def publish_message(self,sender_id, groupe_a_contacter, message_a_ecrire):
        n_id = max([mess.id for mess in self.get_messages()])+1
        self.get_messages().append(Message(n_id,'10:55, 12/12/2024',int(sender_id),int(groupe_a_contacter),message_a_ecrire))
        print(self.get_messages())
        self.save_server()
    
    @override
    def add_member_server(self, id_to_add, channel_id):
        for channel in self.get_channels():
            if int(channel_id) == channel : 
                for user in self.get_users():
                    if user.id not in channel.member_ids:
                        print(User(user.id, user.name))
            channel.member_ids.append(int(id_to_add))
        self.save_server()

    @override
    def channel_creation(self,name_group,members):
        for user in self.get_users() :
            print(User(user.id, user.name))
        n_id = max([c.id for c in self.get_channels()])+1
        self.get_channels().append(Channel(n_id, name_group, members))
        print(Channel(n_id, name_group, members))
        self.save_server()