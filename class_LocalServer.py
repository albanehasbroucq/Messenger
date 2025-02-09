# Une bonne pratique est de séparer ses imports en 2 :
# - d'abord les imports de bibliothèques
# - puis les imports de fichiers que vous avez écrits dans votre projet
from datetime import datetime
import json
from typing import override

from classes_User_Channel_Message import User, Channel, Message
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

        # Si vous avez une valeur de return, il faut penser à indiquer son type
        # dans la signature de la fonction. Ici vous n'utilisez
        # pas le return, vous pouvez donc l'enlever.

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
    def add_user(self, nom: str) -> None:
        n_id = max([u.id for u in self.get_users()])+1
        self.get_users().append(User(n_id,nom))
        self.save_server()

    @override
    # Puisque le constructeur Message.__init__ attend des int,
    # vous pouvez spécifier que votre fonction publish_message
    # attend également des int.
    # Lorsque vous utilisez la fonction, vous saurez alors qu'il
    # faut commencer par convertir les str en int.
    def publish_message(self,sender_id: int, groupe_a_contacter: int, message_a_ecrire: str) -> None:
        n_id = max([mess.id for mess in self.get_messages()])+1
        # Pour interagir avec des horodatages, vous pouvez utiliser le
        # module datetime. Il possède des fonctionnalités avancées
        # pour parser et formater des dates, mais un simple appel à
        # str permet déjà d'obtenir un premier rendu correct.
        self.get_messages().append(Message(n_id,str(datetime.now()), sender_id, groupe_a_contacter,message_a_ecrire))
        print(self.get_messages())
        self.save_server()
    
    @override
    def add_member_server(self, id_to_add: int, channel_id: int) -> None:
        # Cette fonction était bugguée : elle ajoutait l'utilisateur
        # à tous les channels
        for channel in self.get_channels():
            # Cette condition n'était jamais vraie, car channel
            # est un Channel, et channel_id un int
            if channel_id == channel.id:
                if id_to_add not in channel.member_ids:
                    # Ce append était effectué sur tous les channel
                    channel.member_ids.append(id_to_add)
        self.save_server()

    @override
    def channel_creation(self,name_group: str,members: list[int]) -> None:
        for user in self.get_users() :
            print(User(user.id, user.name))
        n_id = max([c.id for c in self.get_channels()])+1
        self.get_channels().append(Channel(n_id, name_group, members))
        print(Channel(n_id, name_group, members))
        self.save_server()