import requests
import json
from classes_User_Channel_Message import User, Channel, Message

class Server:
    # Pas besoin de déclarer __init__ et __repr__. Vous n'avez besoin
    # de déclarer que les fonctions qui sont appelées explicitement
    # sur des Server

    def get_users(self)-> list[User]:
        # Nous n'avons pas vu les exceptions en cours,
        # mais elles permettent de remonter des erreurs d'exécutions.
        # Ici ce code n'est pas censé être atteint, car la fonction
        # sera toujours appelée sur une sous-classe qui la redéfinira.
        # Si on oublie de la redéfinir, l'erreur sera assez explicite
        # (Not implemented)
        raise NotImplementedError()

    def get_channels(self)-> list[Channel]:
        raise NotImplementedError()
    
    def get_messages(self)-> list[Message]:
        raise NotImplementedError()

    # N'oubliez pas de typer vos fonctions
    def add_user(self, nom: str) -> None:
        raise NotImplementedError()

    def publish_message(self,sender_id: int, groupe_a_contacter: int, message_a_ecrire: str) -> None:
        raise NotImplementedError()

    def add_member_server(self, id_to_add: int, channel_id: int) -> None:
        raise NotImplementedError()

    def channel_creation(self,name_group: str, members: list[int]) -> None:
        raise NotImplementedError()
