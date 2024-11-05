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

print('=== Messenger ===')
print('1. See users')
print('2. See channels')
print('x. Leave')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == '1':
    print( 'User list :')
    for u in server['users']:
        print((str(u['id']))+'.'+u['name'])
    print('n. Create user')
    print('x. Main menu')
    choice = input('Select an option: ')

elif choice == '2':
    for c in server['channels']:
        print((str(c['id']))+'.'+c['name'])

else:
    print('Unknown option:', choice)

if choice == 'n':
    nom = input('Choisir un nom:')
    n_id = max([d['id'] for d in server['users']])+1
    server['users'].append({'id': n_id, 'name' : nom})
    print(server['users'])

elif choice == 'x' :
    