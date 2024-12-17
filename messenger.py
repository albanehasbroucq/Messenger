from datetime import datetime
import json
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

SERVER_FILE_NAME= 'server-data.json'
server_as_class = Server('Messenger', [],[],[])
server_as_class.load_server()

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
    
class Interaction:
    def __init__(self, serv : Server)
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


### FICHIER JSON ET CONVERSION: 


### DÉFINTIIONS DES FONCTIONS UTILES AU SERVER:


def user_affichage():
    print( 'User list :')
    for u in server_as_class.users:
        print(User(u.id, u.name))
    print('n. Create user')
    print('x. Main menu')
    choice = input('Select an option: ')
    if choice == 'x':
        retour_menu()
    elif choice == 'n':
        new_user()
    accueil()

def affichage_membre_groupe():
    group= input('Les membres de quel groupe veux-tu afficher ?')
    for g in server_as_class.channels:
        if g.name == group:
            ids= g.member_ids
            for u in server_as_class.users:
                if u.id in ids:
                    print(User(u.id,u.name))
    accueil()

def add_member():
    channel_id = input('Numéro id du groupe où ajouter:')
    for channel in server_as_class.channels:
        if int(channel_id)== channel.id : 
            for user in server_as_class.users:
                if user.id not in channel.member_ids:
                    print(User(user.id, user.name))
            id_to_add = input('Quel id ajouter :')
            channel.member_ids.append(int(id_to_add))
            print(channel)
    accueil()
    server_as_class.save_server()

def create_channel():
    name_group = input('Choose a name of group:')
    for user in server_as_class.users :
        print(User(user.id, user.name))
    members = input('Give the ids you want in the group:')
    liste_membres_id_str = members.split(',')
    liste_membres_id = []
    for id in liste_membres_id_str:
        liste_membres_id.append(int(id)) 
    n_id = max([c.id for c in server_as_class.channels])+1
    server_as_class.channels.append(Channel(n_id, name_group, liste_membres_id))
    print(Channel(n_id, name_group, liste_membres_id))
    server_as_class.save_server()
    accueil()

def channels_affichage():
    for c in server_as_class.channels:
        print(Channel(c.id,c.name, c.member_ids))
    print('c. Create channel')
    print('a. Add a member to a channel')
    print("l. Liste les membres d'un groupe")
    print('x. Main menu')
    choice = input('Select an option: ')
    if choice == 'c':
        create_channel()
    elif choice == 'a':
        add_member()
    elif choice == 'l':
        affichage_membre_groupe()
    elif choice == 'x':
        leave()
    else:
        print('Unknown option:', choice)
        return None

def new_user():
    nom = input('Choisir un nom:')
    n_id = max([u.id for u in server_as_class.users])+1
    server_as_class.users.append(User(n_id,nom))
    server_as_class.save_server()
    accueil()

def send_message():
    for users in server_as_class.users:
        print(User(users.id, users.name))
    sender_id = input('quel est ton id:')
    for groupe in server_as_class.channels:
        if int(sender_id) in groupe.member_ids :
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    groupe_a_contacter = input('à quel groupe veux-tu écrire (id de groupe):')
    message_a_ecrire = input('Que veux tu écrire:')
    n_id = max([mess.id for mess in server_as_class.messages])+1
    server_as_class.messages.append(Message(n_id,'10:55, 12/12/2024',int(sender_id),int(groupe_a_contacter),message_a_ecrire))
    print(server_as_class.messages)
    server_as_class.save_server()
    accueil()

def read_message():
    for users in server_as_class.users:
        print(User(users.id, users.name))
    sender_id = input('quel est ton id:')
    for groupe in server_as_class.channels:
        if int(sender_id) in groupe.member_ids:
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    groupe_a_consulter = input('Les messages de quel groupe veux-tu voir (id de groupe):')
    for groupe in server_as_class.channels:
        if groupe.id == int(groupe_a_consulter):
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    for mess in server_as_class.messages:
        #if mess['channel']== int(groupe_a_consulter):
            #for id in mess['id']:
            #    print 
        if mess.channel == int(groupe_a_consulter):
            for user in server_as_class.users:
                if user.id == mess.sender_id:
                    print(User(user.id ,user.name))
                    message = Message(mess.id, mess.sender_id, mess.channel, mess.reception_date, mess.content)
                    print(message)

    print('----------------------')
    print('3. Send a message')
    print('x. Main menu')
    choice = input('Select an option: ')
    if choice == '3':
        send_message()
    elif choice == 'x':
        retour_menu()
    else: 
        leave()


### ENREGISTREMENT SUR LE SERVER ET CONVERSION JSON-DICT:
   
accueil()

#test