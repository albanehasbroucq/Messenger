from datetime import datetime
import json
import requests

### DÉFINITIONS DES CLASSES :

class User:
    def __init__(self,id:int, name:str):
        self.id = id
        self.name = name

    def __repr__(self) -> str :
        return f'User(id={self.id}, name={self.name})'

    def to_dict(self):
        dict = {'id' : self.id, 'name' : self.name}
        return dict


class Channel:
    def __init__(self,id:int, name:str, member_ids : list):
        self.id = id
        self.name = name
        self.member_ids = member_ids
    def __repr__(self) -> str :
        return f'Channel(id={self.id}, name={self.name}, member_ids={self.member_ids})'
    
    def to_dict(self):
        dict = {'id' : self.id, 'name' : self.name, 'member_ids': self.member_ids}
        return dict


class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int, content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content

    def __repr__(self) -> str :
        return f'Message(id={self.id}, sender_id={self.sender_id}, channel={self.channel}, content={self.content})'

    def to_dict(self):
        dict = {'id' : self.id, 'reception_date' : self.reception_date, 'sender_id': self.sender_id, 'channel': self.channel, 'content': self.content}
        return dict


class Server:
    def __init__(self, name:str, users: list[User], channels: list[Channel], messages: list[Message]):
        self.name=name
        self.users=users
        self.channels=channels
        self.messages=messages
    
    def __repr__(self) -> str:
        return f'Server(name={self.name}, users={self.users}, channels={self.channels})'
    
    def load_server(self):
        with open(SERVER_FILE_NAME) as json_file:
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
    def save_server(self):
        dic={}
        dic['users'] = [user.to_dict() for user in server_as_class.users]
        dic['channels'] = [channel.to_dict() for channel in server_as_class.channels]
        dic['messages'] = [mess.to_dict() for mess in server_as_class.messages]
        with open(SERVER_FILE_NAME, 'w') as fichier:
            json.dump(dic, fichier, indent=4, ensure_ascii=False)

    def get_users(self):
        return(self.users)
    def get_channels(self):
        return(self.channels)
    def get_messages(self):
        return(self.messages)
    #def add_message(self, message:Message):

class Interaction:
    def __init__(self, serv:"RemoteServer"):
        self.server=serv

    def accueil(self):
        print('=== Messenger ===')
        print('1. See users')
        print('2. See channels')
        print('3. Send a message')
        print('4. See messages')
        print('x. Leave')
        choice = input('Select an option: ')
        if choice == 'x':
            self.leave()
        elif choice == '1':
            self.user_affichage()
        elif choice == '2':
            self.channels_affichage()
        elif choice == '3':
            self.send_message()
        elif choice == '4':
            self.read_message()
        else:
            print('Unknown option:', choice)
            return None

    def leave(self):
        print('Bye!')
        return None

    def retour_menu(self):
        self.accueil()

    def read_message(self):
        for users in self.server.get_users():
            print(User(users.id, users.name))
        sender_id = input('quel est ton id:')
        for groupe in self.server.get_channels():
            if int(sender_id) in groupe.member_ids:
                print(Channel(groupe.id, groupe.name, groupe.member_ids))
        groupe_a_consulter = input('Les messages de quel groupe veux-tu voir (id de groupe):')
        for groupe in self.server.get_channels():
            if groupe.id == int(groupe_a_consulter):
                print(Channel(groupe.id, groupe.name, groupe.member_ids))
        for mess in self.server.get_messages():
            #if mess['channel']== int(groupe_a_consulter):
                #for id in mess['id']:
                #    print 
            if mess.channel == int(groupe_a_consulter):
                for user in self.server.get_users():
                    if user.id == mess.sender_id:
                        print(User(user.id ,user.name))
                        message = Message(mess.id, mess.sender_id, mess.channel, mess.reception_date, mess.content)
                        print(message)

        print('----------------------')
        print('3. Send a message')
        print('x. Main menu')
        choice = input('Select an option: ')
        if choice == '3':
            self.send_message()
            
        elif choice == 'x':
            self.retour_menu()
        else: 
           self.leave()

    def send_message(self):
        for users in self.server.get_users():
            print(User(users.id, users.name))
        sender_id = input('quel est ton id:')
        for groupe in self.server.get_channels():
            if int(sender_id) in groupe.member_ids :
                print(Channel(groupe.id, groupe.name, groupe.member_ids))
        groupe_a_contacter = input('à quel groupe veux-tu écrire (id de groupe):')
        message_a_ecrire = input('Que veux tu écrire:')
        n_id = max([mess.id for mess in self.server.get_messages()])+1
        self.server.get_messages().append(Message(n_id,'10:55, 12/12/2024',int(sender_id),int(groupe_a_contacter),message_a_ecrire))
        print(self.server.get_messages())
        self.server.save_server()
        self.accueil()

    def channels_affichage(self):
        for c in self.server.get_channels():
            print(Channel(c.id,c.name, c.member_ids))
        print('c. Create channel')
        print('a. Add a member to a channel')
        print("l. Liste les membres d'un groupe")
        print('x. Main menu')
        choice = input('Select an option: ')
        if choice == 'c':
            self.create_channel()
        elif choice == 'a':
            self.add_member()
        elif choice == 'l':
            self.affichage_membre_groupe()
        elif choice == 'x':
            self.leave()
        else:
            print('Unknown option:', choice)
            return None
        
    def user_affichage(self):
        print( 'User list :')
        for u in self.server.get_users() :
            print(User(u.id, u.name))
        print('n. Create user')
        print('x. Main menu')
        choice = input('Select an option: ')
        if choice == 'x':
            self.retour_menu()
        elif choice == 'n':
            self.new_user()
        self.accueil()

    def affichage_membre_groupe(self):
        group= input('Les membres de quel groupe veux-tu afficher ?')
        for g in self.server.channels:
            if g.name == group:
                ids= g.member_ids
                for u in self.server.users:
                    if u.id in ids:
                        print(User(u.id,u.name))
        self.accueil()

    def add_member(self):
        channel_id = input('Numéro id du groupe où ajouter:')
        for channel in self.server.channels:
            if int(channel_id)== channel.id : 
                for user in self.server.users:
                    if user.id not in channel.member_ids:
                        print(User(user.id, user.name))
                id_to_add = input('Quel id ajouter :')
                channel.member_ids.append(int(id_to_add))
                print(channel)
        self.accueil()
        self.server.save_server()

    def create_channel(self):
        name_group = input('Choose a name of group:')
        for user in self.server.users :
            print(User(user.id, user.name))
        members = input('Give the ids you want in the group:')
        liste_membres_id_str = members.split(',')
        liste_membres_id = []
        for id in liste_membres_id_str:
            liste_membres_id.append(int(id)) 
        n_id = max([c.id for c in self.server.channels])+1
        self.server.channels.append(Channel(n_id, name_group, liste_membres_id))
        print(Channel(n_id, name_group, liste_membres_id))
        self.server.save_server()
        self.accueil()

    def new_user(self):
        nom = input('Choisir un nom:')
        n_id = max([u.id for u in self.server.users])+1
        self.server.users.append(User(n_id,nom))
        self.server.save_server()
        self.accueil()


class RemoteServer:

    def __init__(self, url):
        self.url=url

    def get_users(self)-> list[User]:
        response_users=requests.get(self.url+'/users')
        response_users.json()
        return(User(user[int("id")], user["name"]) for user in response_users)

    def get_channels(self)-> list[Channel]:
        response_channels=requests.get(self.url+'/channels')
        response_channels.json()
        return(Channel(channel[int("id")], channel["name"], channel["member_ids"]) for channel in response_channels)
    def get_messages(self)-> list[Message]:
        response_messages=requests.get(self.url+'/messages')
        response_messages.json()
        return(Message(mess[int("id")], mess["reception_date"], mess["sender_id"], mess["channel"], mess["content"]) for mess in response_messages)


SERVER_FILE_NAME= 'server-data.json'
server_as_class = Server('Messenger', [],[],[])
server_as_class.load_server()

server_internet =RemoteServer('http://vps-cfefb063.vps.ovh.net')
interaction = Interaction(server_internet)
interaction.accueil()
