from datetime import datetime
import json
import argparse

### PASSAGE EN ARGUMENT
parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', help = 'enter json path')
args = parser.parse_args()


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

### FICHIER JSON ET CONVERSION: 
SERVER_FILE_NAME = args.server
def load_server():
    with open(SERVER_FILE_NAME) as json_file:
        server=json.load(json_file)

        users = [User(user['id'], user['name']) for user in server['users']]
        server['users'] = users

        channels = [Channel(channel['id'], channel['name'], channel['member_ids'])for channel in server['channels']]
        server['channels'] = channels

        messages = [Message(mess['id'], mess['reception_date'], mess['sender_id'], mess['channel'], mess['content']) for mess in server['messages']]
        server['messages'] = messages
    ## server['users']:list[dict]
    ## Transform server['users'] en list[User]

    return server
#with open(args.server, 'r') as fichier:
#    server = json.load(fichier)

server=load_server()

### DÉFINTIIONS DES FONCTIONS UTILES AU SERVER:

def leave():
    print('Bye!')
    return None

def retour_menu():
    accueil()

def user_affichage():
    print( 'User list :')
    for u in server['users']:
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
    for g in server['channels']:
        if g.name ==group:
            ids= g.member_ids
            for u in server['users']:
                if u.id in ids:
                    print(User(u.id,u.name))
    accueil()

def add_member():
    channel_id = input('Numéro id du groupe où ajouter:')
    for channel in server['channels']:
        if int(channel_id)== channel.id : 
            for user in server['users']:
                if user.id not in channel.member_ids:
                    print(User(user.id, user.name))
            id_to_add = input('Quel id ajouter :')
            channel.member_ids.append(int(id_to_add))
            print(channel)
    accueil()
    save_server()
 
def create_channel():
    name_group = input('Choose a name of group:')
    for user in server['users']:
        print(User(user.id, user.name))
    members = input('Give the ids you want in the group:')
    liste_membres_id_str = members.split(',')
    liste_membres_id = []
    for id in liste_membres_id_str:
        liste_membres_id.append(int(id)) 
    n_id = max([c.id for c in server['channels']])+1
    server['channels'].append(Channel(n_id, name_group, liste_membres_id))
    print(Channel(n_id, name_group, liste_membres_id))
    save_server()
    accueil()

def channels_affichage():
    for c in server['channels']:
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
    n_id = max([u.id for u in server['users']])+1
    server['users'].append(User(n_id,nom))
    save_server()
    accueil()

def send_message():
    for users in server['users']:
        print(User(users.id, users.name))
    sender_id = input('quel est ton id:')
    for groupe in server['channels']:
        if int(sender_id) in groupe.member_ids :
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    groupe_a_contacter = input('à quel groupe veux-tu écrire (id de groupe):')
    message_a_ecrire = input('Que veux tu écrire:')
    n_id = max([mess.id for mess in server['messages']])+1
    server['messages'].append(Message(n_id,'11:46, 07/11/2024',int(sender_id),int(groupe_a_contacter),message_a_ecrire))
    print(server['messages'])
    save_server()
    accueil()

def read_message():
    for users in server['users']:
        print(User(users.id, users.name))
    sender_id = input('quel est ton id:')
    for groupe in server['channels']:
        if int(sender_id) in groupe.member_ids:
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    groupe_a_consulter = input('Les messages de quel groupe veux-tu voir (id de groupe):')
    for groupe in server['channels']:
        if groupe.id == int(groupe_a_consulter):
            print(Channel(groupe.id, groupe.name, groupe.member_ids))
    for mess in server['messages']:
        #if mess['channel']== int(groupe_a_consulter):
            #for id in mess['id']:
            #    print 
        if mess.channel == int(groupe_a_consulter):
            for user in server['users']:
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

def accueil():
    print('=== Messenger ===')
    print('1. See users')
    print('2. See channels')
    print('3. Send a message')
    print('4. See messages')
    print('x. Leave')
    choice = input('Select an option: ')
    if choice == 'x':
        leave()
    elif choice == '1':
        user_affichage()
    elif choice == '2':
        channels_affichage()
    elif choice == '3':
       send_message()
    elif choice == '4':
        read_message()
    else:
        print('Unknown option:', choice)
        return None

### ENREGISTREMENT SUR LE SERVER ET CONVERSION JSON-DICT:
def save_server():
    dic={}
    dic['users'] = [user.to_dict() for user in server['users']]
    dic['channels'] = [channel.to_dict() for channel in server['channels']]
    dic['messages'] = [mess.to_dict() for mess in server['messages']]
    with open(SERVER_FILE_NAME, 'w') as fichier:
        json.dump(dic, fichier, indent=4, ensure_ascii=False)
    
accueil()