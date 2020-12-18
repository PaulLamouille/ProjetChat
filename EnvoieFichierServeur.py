# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:56:31 2020

@author: polor
"""

import socket
import os
import argparse

SEPARATEUR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 70 #4KB

def envoi_fichier(nomFichier, host, port):
    # récupère taille du fichier
    tailleFichier = os.path.getsize(nomFichier)
    # création socket client
    s = socket.socket()
    print(f"[+] Connexion à {host}:{port}")
    s.connect((host, port))
    print("[+] Connecté.")

    # envoi du nomFichier et tailleFichier
    s.send(f"{nomFichier}{SEPARATEUR}{tailleFichier}".encode())
    
    
    # Début de l'envoi du fichier
    print("Envoi de "+nomFichier)
    
    with open(nomFichier, "rb") as f:
        for _ in (range(tailleFichier)):
            # lecture des bytes du fichier
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # l'envoi du fichier est fini
                break
            s.sendall(bytes_read)
            
    print("Envoi de "+nomFichier+" réussi.")   
    
    # fermeture socket
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("--file", help="Nom du fichier à envoyer")
    parser.add_argument("--host", help="Adresse IP du destinataire")
    parser.add_argument("--port", help="Port à utiliser, 5001 est le port par défaut", default=5001)
    args = parser.parse_args()
    nomFichier = args.file
    host = args.host
    port = args.port
    envoi_fichier(nomFichier, host, port)