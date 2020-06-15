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

# lista cu utilizatorii conectati
connectedUsers = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#declar o lista cu posibili utilizatori - accestia sunt toti utilizatorii
users = [
    ("1", "Cosmin"),
    ("2", "Alin"),
    ("3", "Nico")
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
            print(f"received a new message: {msg}" + " //the end")
            if not authenticated:
                user = msg
                #verific daca exista in lista de useri
                for u in users:
                    if u[0] == user:
                        print("connected with user: " + u[1])
                        connectedUser = ((u[0], u[1]), (conn, addr))
                        authenticated = True
                        conn.send(AUTH_SUCCESS.encode(FORMAT))
                        connectedUsers.append((u, (conn, addr)))
                        #trimit lista cu toti utilizatorii
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
                        print("Currently connected users: ")
                        for c in connectedUsers:
                            print(c)
                if not authenticated:
                    print("user not found, sending message to client")
                    conn.send(AUTH_FAIL.encode(FORMAT))
                    authenticated = True


            if msg == DISCONNECT_MESSAGE:
                connected = False
                print("removing user: " + connectedUser[0][1])
                print(connectedUser)
                connectedUsers.remove(connected)

    conn.close()
            

def start():
    print(SERVER)
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def send_message(msg, conn, addr):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

print("Starting server...")
start()


