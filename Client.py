
import socket
import threading
from EnvoieFichierServeur import envoi_fichier
from EnvoieFichierClient import recv_file
from tkinter import *
from datetime import datetime
import pickle

loged = False


window = Tk()
window.title("Chat")
window.geometry('400x600')

root = window
login_client = StringVar()
login_client.set("")
ip_client = StringVar()
ip_client.set("")
date_connection_client = StringVar()
date_connection_client.set("")

lbl_title = Label(window, text="Connect by entering 'log USERNAME PASSWORD'")
lbl_title.pack()


def clicked():
    global left, login_commande
    text_chat = "You said \"" + txt.get() + "\""
    login_commande = txt.get() 
    left = not left

messages_frame = Frame(window)
scrollbar = Scrollbar(messages_frame)  
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

lbl_space0 = Label(window, text="")
lbl_space0.pack()

lbl_say = Label(window, text="Say something : ")
lbl_say.pack()

txt = Entry(window,width=20)
txt.pack()


host="127.0.0.1"
port=5001
client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive():
    while True:        
        strdatenow.set("We are the " + datetime.now().strftime("%B %d, %Y %H:%M:%S"))
        try:
            message=client.recv(1024).decode('ascii')
            msg_list.insert(END, message)
            if len(message.split(':')) == 1:
                msg_list.itemconfigure(msg_list.size() - 1, foreground='brown')
            else:
                namepossible=message.split(':')[0]
                namepossible = namepossible[0:len(namepossible)-1]
                if namepossible == login_client.get():
                    msg_list.itemconfigure(msg_list.size() - 1, bg='lightgray')
            
            if message == "rcv":
                recv_file()
                continue
        except Exception as e:
            print(e)
            print("An error occured")
            client.close()
            break
        
        
def write(event = None):
    global loged
    message = txt.get()
    txt.delete(0, END)
    txt.insert(0, "")
    client.send(message.encode('ascii'))
    
    if not loged:
        file = open("shared.pkl", 'rb')
        shared = pickle.load(file)
        file.close()
        
        if shared["date_connection"] != "":
            loged = True
            login_client.set(shared["login"])
            ip_client.set(shared["ip"])
            date_connection_client.set("Connection date\n" + shared["date_connection"])
            print(login_client.get(), loged)
            lbl_title["text"]="Welcome " + shared["login"]

    if message[0:3] == "snd":
        arg = message.split(' ')[1].strip()
        envoi_fichier(arg, host)
        



btn = Button(window, text="Send", command=write)
btn.pack()

lbl_space1 = Label(window, text="")
lbl_space1.pack()
lbl_space2 = Label(window, text="")
lbl_space2.pack()
lbl_space3 = Label(window, text="")
lbl_space3.pack()
lbl_space4 = Label(window, text="")
lbl_space4.pack()


lbl_login = Label(window, textvariable=login_client)
lbl_login.pack()

lbl_ip = Label(window, textvariable=ip_client)
lbl_ip.pack()

lbl_space5 = Label(window, text="")
lbl_space5.pack()

lbl_date = Label(window, textvariable=date_connection_client)
lbl_date.pack()

strdatenow = StringVar()
strdatenow.set("We are the " + datetime.now().strftime("%B %d, %Y %H:%M:%S"))
lbl_datenow = Label(window, textvariable=strdatenow)
lbl_datenow.pack(side=BOTTOM)

receive_thread= threading.Thread(target=receive)
receive_thread.start()

window.mainloop()
