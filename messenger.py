from datetime import datetime

server = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3, 'name': 'Third user'},
        {'id': 4, 'name': '4'},
        {'id': 5, 'name':'5 u'}
    ],
    'channels': [
        {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
    ],
    'messages': [
        {
            'id': 1,
            'reception_date': datetime.now(),
            'sender_id': 1,
            'channel': 1,
            'content': 'Hi 👋'
        }
    ]
}

def leave():
    print('Bye!')
    return None
def retour_menu():
    accueil()

def user_affichage():
    print( 'User list :')
    for u in server['users']:
        print((str(u['id']))+'.'+u['name'])
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
        if g['name']==group:
            ids= g['member_ids']
            for d in server['users']:
                if d['id'] in ids:
                    print(d['name'])
    #ou placer le else ???? unknown group
    accueil()

def add_member():
    group = input('Nom du groupe où ajouter:')
    for d in server['users']:
        print(d['name'], ":", d['id'])
    id_to_add = input('Quel id ajouter :')
    for d in server['channels']:
        if d['name']==group:
            d['member_ids'].append(int(id_to_add))
            print(d['member_ids'])
    else :
        print('Unkonw group')

    accueil()



def create_channel():
    name_group = input('Choose a name of group:')
    members = input('Give the members of the group:')
    liste_membres_name= members.split(',')
    liste_membres_id=[]
    for name in liste_membres_name :
        for d in server['users']:
            if d['name']==name:
                liste_membres_id.append(d['id'])
    n_id = max([d['id'] for d in server['channels']])+1
    server['channels'].append({'id':n_id, 'name': name_group, 'member_ids': liste_membres_id})
    accueil()



def channels_affichage():
    for c in server['channels']:
        print((str(c['id']))+'.'+c['name'])
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
    n_id = max([d['id'] for d in server['users']])+1
    server['users'].append({'id': n_id, 'name' : nom})
    accueil()

def message():
    for users in server['users']:
        print(users['name'], ":", users['id'])
    sender_id = input('quel est ton id:')
    for groupe in server['channels']:
        if int(sender_id) in groupe['member_ids']:
            print(groupe['name'], ":", groupe['id'])
    groupe_a_contacter = input('à quel groupe veux-tu écrire (id de groupe):')
    message_a_ecrire = input('Que veux tu écrire:')
    n_id = max([mess['id'] for mess in server['messages']])+1
    server['messages'].append({
        'id': n_id,
        'reception_date': datetime.now(),
        'sender_id': sender_id,
        'channel': groupe_a_contacter,
        'content': message_a_ecrire
    })
    accueil()

def accueil():
    print('=== Messenger ===')
    print('1. See users')
    print('2. See channels')
    print('3. Send a message')
    print('x. Leave')
    choice = input('Select an option: ')
    if choice == 'x':
        leave()
    elif choice == '1':
        user_affichage()
    elif choice == '2':
        channels_affichage()
    elif choice == '3':
        message()
    else:
        print('Unknown option:', choice)
        return None


accueil()

