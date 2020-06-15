import socket


HEADER = 64
PORT = 5050
SERVER = "192.168.0.101"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

test = [
    ("1", ("2", "3")),
    ("4", ("5", "6"))
]

test2 = [
    ("1", "Cosmin"),
    ("4", "Nico"),
    ("3", "a"),
    ("2", "b")
]

usr = ()

users_msg = ""
for t2 in test2:
     print(t2[1])
     if t2[0] == "4":
         usr = t2[0], t2[1]
         continue
     print(t2[1])


print(usr)

test2.remove(usr)


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)

# def receive():
#     connected = True
#     while connected:
#         msg_length = client.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = client.recv(msg_length).decode(FORMAT)
#             print(f"client received new message: {msg}, length: {msg_length}")


# send("Hello server.")
# receive()