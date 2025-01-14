from datetime import datetime
import json
import requests
from argparse import ArgumentParser
### DÉFINITIONS DES CLASSES :

# from portailserver import PortailServer
from class_RemoteServer import RemoteServer
from class_Server import Server
from class_Interaction import Interaction
from classes_User_Channel_Message import User, Channel, Message

argument_parser = ArgumentParser()
argument_parser.add_argument('-f', '--filename')
argument_parser.add_argument('-u', '--url')
argument_parser.add_argument('-p', '--portail', action = 'store_true')
arguments = argument_parser.parse_args()
server : Server
if arguments.filename is not None:
    server = Server(arguments.filename)
elif arguments.url is not None:
    server = RemoteServer(arguments.url)
#elif arguments.portail is not None:
#    server = PortailServer()
else : 
    print("error : -f or -u should be set")
    exit(-1)


server.load_server()
client = Interaction(server)
client.accueil()

# SERVER_FILE_NAME= 'server-data.json'
# server_as_class = Server('Messenger', [],[],[])
# server_as_class.load_server()

# server_internet = RemoteServer('http://vps-cfefb063.vps.ovh.net')
# interaction = Interaction(server_internet)
# interaction.accueil()
