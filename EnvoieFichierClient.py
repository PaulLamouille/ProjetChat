# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:56:26 2020

@author: polor
"""

import socket

import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATEUR = "<SEPARATOR>"
# creation socket server
# TCP socket
s = socket.socket()
# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Ecoute à {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 

print(f"[+] {address} est connecté.")

# reception des informations des fichiers
received = client_socket.recv(BUFFER_SIZE).decode()
nomFichier, tailleFichier = received.split(SEPARATEUR)
extension=nomFichier.split('.')

# remove absolute path if there is
nomFichier = os.path.basename(nomFichier)
tailleFichier = int(tailleFichier)
new_Fichier='test2.'+extension[-1]
# debut reception du fichier du socket
# ecriture dans un nouveau fichier 'test2.txt'

print('Reception du fichier '+nomFichier)
with open(new_Fichier, "wb") as f:
    for _ in (range(tailleFichier)):
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # si rien n'est reçu on arrête la transmisison de fichier
            
            break
        # ecriture dans le fichier des bytes recus
        f.write(bytes_read)
        
print('Réception du fichier '+nomFichier+' terminée') 
print('Un fichier au nom de test2.txt à été ajouté à votre répertoire')  
      
        

# fermeture socket client
client_socket.close()
# fermeture socket serveur
s.close()