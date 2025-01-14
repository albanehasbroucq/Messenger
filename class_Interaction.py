from classes_User_Channel_Message import User, Channel, Message
from class_RemoteServer import RemoteServer
from class_Server import Server
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
        self.server.publish_message(sender_id, groupe_a_contacter, message_a_ecrire)
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
        group= input('Les membres de quel groupe veux-tu afficher ?(nom)')
        for g in self.server.get_channels():
            if g.name == group:
                ids= g.member_ids
                for u in self.server.get_users():
                    if u.id in ids:
                        print(User(u.id,u.name))
        self.accueil()

    def add_member(self):
        channel_id = input('Numéro id du groupe où ajouter:')
        id_to_add = input('Quel id ajouter :')
        # for channel in self.server.get_channels():
        #     if int(channel_id)== channel : 
        #         for user in self.server.get_users():
        #             if user.id not in channel.member_ids:
        #                 print(User(user.id, user.name))
                # channel.member_ids.append(int(id_to_add))
        self.server.add_member_server(id_to_add, channel_id)
        self.accueil()


    def create_channel(self):
        name_group = input('Choose a name of group:')
        members = input('Give the ids you want in the group:')
        self.server.channel_creation(name_group, members)
        # for user in self.server.get_users() :
        #     print(User(user.id, user.name))

        # liste_membres_id_str = members.split(',')
        # liste_membres_id = []
        # for id in liste_membres_id_str:
        #     liste_membres_id.append(int(id)) 
        # n_id = max([c.id for c in self.server.get_channels()])+1
        # self.server.get_channels().append(Channel(n_id, name_group, liste_membres_id))
        # print(Channel(n_id, name_group, liste_membres_id))
        # self.server.save_server()
        self.accueil()

    def new_user(self):
        nom = input('Choisir un nom:')
        self.server.add_user(nom)
        # n_id = max([u.id for u in self.server.get_users()])+1
        # self.server.get_users().append(User(n_id,nom))
        # self.server.save_server()
        self.accueil()

