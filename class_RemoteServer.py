import requests
import json
from class_Server import Server
from classes_User_Channel_Message import User, Channel, Message
from typing import override

class RemoteServer(Server):
    @override
    def __init__(self, url):
        self.url=url

    @override
    def get_users(self)-> list[User]:
        # N'oubliez pas de vérifier que le code de réponse HTTP
        # (response_users.status_code) vaut 200
        response_users=requests.get(self.url+'/users')
        # Pour faire une liste, il faut entourer l'expression de crochets
        return [User(user[("id")], user["name"]) for user in response_users.json()]

    @override
    def get_channels(self)-> list[Channel]:
        response_channels=requests.get(self.url+'/channels')
        channels=[]
        for channel in response_channels.json():
            id, name = channel["id"], channel["name"]
            response_memeber_ids=requests.get(self.url+f'/channels/{id}/members')
            member_ids = [member["id"] for member in response_memeber_ids.json()]
            channels.append(Channel(id, name, member_ids))
        return channels
    
    @override
    def get_messages(self)-> list[Message]:
        response_messages=requests.get(self.url+'/messages')
        return [Message(mess[("id")], mess["reception_date"], mess["sender_id"], mess["channel_id"], mess["content"]) for mess in response_messages.json()]
    
    @override
    def add_user(self, nom: str) -> None:
        requests.post(self.url+'/users/create', json={"name": nom})

    # Vous n'avez pas défini cette méthode dans la classe mère (Server),
    # ce n'est donc pas un "override".
    def deleting_user(self, user_to_delete_id: int) -> None:
        response=requests.delete(self.url+f'/users/{user_to_delete_id}')
        if response.status_code != 200:
            print ("Cette fonction n'est pas encore disponible")

    @override
    def publish_message(self,sender_id: int, groupe_a_contacter: int, message_a_ecrire: str) -> None:
        requests.post(self.url+f'/channels/{groupe_a_contacter}/messages/post', json={"sender_id": sender_id, "channel": groupe_a_contacter,"content":message_a_ecrire})

    @override
    def add_member_server(self, id_to_add, channel_id):
        requests.post(self.url+f'/channels/{channel_id}/join', json={"user_id": id_to_add})

    @override
    def channel_creation(self, name_group: str, members: list[int]) -> None:
        requests.post(self.url+'/channels/create', json={"name": name_group})
        # Attention, rien n'empêche 2 canaux différents d'avoir le même nom.
        # La requête POST renvoie l'identifiant du canal nouvellement créé,
        # vous auriez pu l'utiliser directement.
        for channel in self.get_channels():
            if channel.name == name_group:
                id_group= channel.id
        for member in members:
            self.add_member_server(member,id_group)
    