import socket
import threading
import time
from datetime import date

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
AUTH_SUCCESS = "USER_AUTHENTICATED"
AUTH_FAIL = "USER_NOT_AUTHENTICATED"
MSG_SIZE = 100
CONTACTS_START = "CONTACTS_LIST_STARTED"
CONTACTS_FINISH = "CONTACTS_LIST_FINISHED"
CONTACT_LIST_ITEM = 10000

print(SERVER)

#lista cu utilizatorii conectati
connectedUsers = []

#lista cu mesaje care trebuie trimise cand o persoana se conecteaza
messagesQueue = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#lista cu posibili utilizatori - accestia sunt toti utilizatorii
users = [
    ("1", "Cosmin"),
    ("2", "Ionel"),
    ("3", "Gheorghe")
]

def handle_client(conn, addr):
    print(f"new connection from adress: {addr} established")
    connectedUser = (())
    user = ''
    authenticated = False
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            if msg == DISCONNECT_MESSAGE:
                print("Disconnect signal received. Ending connection...")
                connected = False
                print("removing user: " + connectedUser[0][1])
                print(connectedUser)
                connectedUsers.remove(connectedUser)
            else:
                print(f"received a new message: {msg}" + " //the end")
                if not authenticated:
                    user = msg
                    #verific daca exista in lista de useri
                    for u in users:
                        if u[0] == user:
                            print("connected with user: " + u[1])
                            connectedUser = ((u[0], u[1]), (conn, addr))
                            authenticated = True
                            user = u
                            conn.send((AUTH_SUCCESS + " ~~~ " + user[0] + " @@@ " + user[1]).encode(FORMAT))
                            connectedUsers.append((u, (conn, addr)))
                            #trimit lista cu toti utilizatorii
                            time.sleep(0.1)
                            conn.send(CONTACTS_START.encode(FORMAT))
                            time.sleep(0.1)
                            users_item = ""
                            for o in users:
                                if u[0] == o[0]:
                                    continue
                                if (len(users_item) + len(o[0] + "///" + o[1]) ) < CONTACT_LIST_ITEM:
                                    users_item += o[0] + "///" + o[1] + "&&&"
                                    continue
                                print("sending the following: " + users_item)
                                conn.send(users_item.encode(FORMAT))
                                users_item = ""
                                time.sleep(0.1)
                            if users_item != "":
                                print("sending the following: " + users_item)
                                conn.send(users_item.encode(FORMAT))
                                time.sleep(0.1)
                            conn.send(CONTACTS_FINISH.encode(FORMAT))
                            time.sleep(0.1)
                            #daca in coada are mesaje, le trimit
                            sentQueuedMessages = []
                            for m in messagesQueue:
                                print("mesaj in coada: " + m[1] + " pentru utilizatorul " + m[0][1])
                                if m[0][0] == user[0] :
                                    print("trimit mesajul " + m[1])
                                    conn.send(m[1].encode(FORMAT))
                                    time.sleep(0.1)
                                    sentQueuedMessages.append(m)
                            #sterg mesajele trimise
                            for m in sentQueuedMessages:
                                messagesQueue.remove(m)

                    if not authenticated:
                        print("user not found, sending message to client")
                        conn.send(AUTH_FAIL.encode(FORMAT))
                        authenticated = False
                else:
                    #trimit mesajul catre destinatar
                    #obtin destinatarul din mesajul primit
                    msgUser = msg.split("~~~")
                    message = msgUser[0].strip()
                    userID = msgUser[1].split("@@@")[0].strip()
                    userName = msgUser[1].split("@@@")[1].strip()

                    #formez mesajul de trimis
                    messageToSend = message + " ~~~ " + user[0] + " @@@ " + user[1]
                    print("Prepared message to be sent: " + messageToSend)


                    #trimit mesajul utilizatorului
                    send_message(messageToSend, userID, userName)
                    

                    #il adaug in lista de mesaje care trebuie trimise cand se conecteaza

                print("Currently connected users: ")
                for c in connectedUsers:
                    print(c[0])

    conn.close()
            

def start():
    print(SERVER)
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def send_messages(msg, user):
        message = msg.encode(FORMAT)
        try:
            user[1][1].send(message)
            time.sleep(10)
        except:
            #ceva nu este in regula cu conexiunea, o sterg
            connectedUsers.remove(user)
            

def send_message(msg, targetUserId, targetUserName):
    message_sent = False
    for c in connectedUsers:
        if c[0][0] == targetUserId:
            print("found a connected user matching the same id: " + c[0][0] + " " + c[0][1])
            #daca este conectat, trimit catre toate conexiunile
            message = msg.encode(FORMAT)
            try:
                c[1][0].send(message)
                time.sleep(0.1)
                message_sent = True
            except:
                #ceva nu este in regula cu conexiunea, o sterg
                connectedUsers.remove(c)
    if message_sent is False:
        #nicio conexiune nu mai era activa
        print("Mesajul nu a putut fi trimis fiindca nu exista nicio conexiune activa.")
        #adaug la coada de mesaje care trebuie trimise
        messagesQueue.append(((targetUserId, targetUserName), msg))



print("Starting server...")
start()


