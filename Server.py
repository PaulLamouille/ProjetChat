
import threading
import socket
from log import add_log
from user import signup, signin
from EnvoieFichierClient import recv_file
from EnvoieFichierServeur import envoi_fichier
from datetime import datetime

host="127.0.0.1"
port=5001

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

addresses=[]
clients=[]
nicknames=[]




def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            index=clients.index(client)
            nickname=nicknames[index]

            message, address = client.recvfrom(1024)
            message = message.decode("ascii")

            if message[0:3]=='snd':
                file = recv_file()
                broadcast("rcv".encode('ascii'))
                for client in clients:
                    thread = threading.Thread(target=envoi_fichier, args=(file, addresses[index]))
                    thread.start()
                continue

            add_log(nickname, address[0], "TXT")
            message = "{} : {}".format(nickname, message)
            message = message.encode("ascii")
            broadcast(message)
            
        except Exception as e:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break
        
        
def receive():
    while True:
        nickname=""

        client, address=server.accept()
        #print(f"Connect with " +str(address))
        add_log(nickname, address[0], "CON")
        
        log=-1
        while log != 0:
            messageTexte = client.recv(1024).decode('ascii').strip()

            if messageTexte[0:3]=='log':
                arg=messageTexte.split(' ')[1:3]
                log=signin(arg[0],arg[1])
                nickname = arg[0]
                add_log(nickname, address[0], "CON")
                
                if log==0:
                    client.send(f'Success log'.encode('ascii'))
                    str_welcolm = "Bienvenue sur le chat  " + arg[0] + "  le  " + datetime.now().strftime("%B %d, %Y %H:%M:%S") + "  ip :  " + address[0] + "  "
                    client.send(f'{str_welcolm}'.encode('ascii'))
                    
                elif log==1:
                    client.send(f'Incorrect Password'.encode('ascii'))
                else:
                    signup(arg[0],arg[1])
                    client.send(f'Created an account'.encode('ascii'))
                    str_welcolm = "Bienvenue sur le chat  " + arg[0] + "  le  " + datetime.now().strftime("%B %d, %Y %H:%M:%S") + "  ip :  " + address[0] + "  "
                    client.send(f'{str_welcolm}'.encode('ascii'))
                    log = 0

        nicknames.append(nickname)
        clients.append(client)
        addresses.append(address[0])
        
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        
        thread= threading.Thread(target= handle, args=(client,))
        thread.start()
        
print('server is listening...')
receive()

























'''

import threading
import socket


from log import add_log
from user import signup, signin
from EnvoieFichierClient import recv_file
from EnvoieFichierServeur import envoi_fichier

host="127.0.0.1"
port=5001

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

addresses=[]
clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            index=clients.index(client)
            nickname=nicknames[index]

            message, address = client.recvfrom(1024)
            message = message.decode("ascii")

            if message[0:3]=='snd':
                file = recv_file()
                broadcast("rcv".encode('ascii'))
                for client in clients:
                    thread = threading.Thread(target=envoi_fichier, args=(file, addresses[index]))
                    thread.start()

                continue



            add_log(nickname, address[0], "TXT")
            message = "{} : {}".format(nickname, message)
            message = message.encode("ascii")
            broadcast(message)
        except Exception as e:
            print(e)
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        nickname=""

        client, address=server.accept()
        print(f"Connect with " +str(address))
        add_log(nickname, address[0], "CON")
        
        log=-1
        while log != 0:
            messageTexte = client.recv(1024).decode('ascii').strip()

            if messageTexte[0:3]=='log':
                arg=messageTexte.split(' ')[1:3]
                log=signin(arg[0],arg[1])
                nickname = arg[0]
                add_log(nickname, address[0], "CON")
                if log==0:
                    client.send(f'Success log'.encode('ascii'))
                elif log==1:
                    client.send(f'Incorrect Password'.encode('ascii'))
                else:
                    signup(arg[0],arg[1])
                    client.send(f'Created an account'.encode('ascii'))
                    log = 0

        nicknames.append(nickname)
        clients.append(client)
        addresses.append(address[0])
        
        print(f'Nickname of the client is '+ nickname)
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server !'.encode('ascii'))
        
        thread= threading.Thread(target= handle, args=(client,))
        thread.start()
print('server is listening...')
receive()

'''














