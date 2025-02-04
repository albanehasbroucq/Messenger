from datetime import datetime
import json
import requests
from argparse import ArgumentParser

# from portailserver import PortailServer
from class_RemoteServer import RemoteServer
from class_LocalServer import LocalServer
from class_Interaction import Interaction
from classes_User_Channel_Message import User, Channel, Message
from class_Server import Server

argument_parser = ArgumentParser()
argument_parser.add_argument('-f', '--filename')
argument_parser.add_argument('-u', '--url')
argument_parser.add_argument('-p', '--portail', action = 'store_true')
arguments = argument_parser.parse_args()
server : Server
if arguments.filename is not None:
    server = LocalServer(arguments.filename)
elif arguments.url is not None:
    server = RemoteServer(arguments.url)
#elif arguments.portail is not None:
#    server = PortailServer()
else : 
    print("error : -f or -u should be set")
    exit(-1)


client = Interaction(server)
client.accueil()

#ancienne version :
# SERVER_FILE_NAME= 'server-data.json'
# server_as_class = Server('Messenger', [],[],[])
# server_as_class.load_server()

# server_internet = RemoteServer('http://vps-cfefb063.vps.ovh.net')
# interaction = Interaction(server_internet)
# interaction.accueil()
