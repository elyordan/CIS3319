from Crypto.Cipher import DES
import socket
import random

#header is the maximum bit number for the message
HEADER = 64
PORT = 5050
#Get the ip address from the local network
SERVER = socket.gethostbyname(socket.gethostname())
#contains the  ip and port
ADDRESS = (SERVER, PORT)
#format in which the bits are encoded or decoded 
FORMAT = 'utf-8'
#message so the server knows that the client gets disconnected so they can connect again
DISCONNECT_MESSAGE = "!DISCONNECTED"
#key used to encript messages
DES_key = str(random.randint(10000000,99999999))

#create a new file with the shared key for the client
def shareKey():
    f = open('key.txt', 'w')
    f.write(DES_key)
    f.close()  

shareKey()


def pad(text):
    n = len(text) % 8
    return text + (b' ' * n)

#server will be equal to a socket stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the server with the address
server.bind(ADDRESS)

#After receiving the client's info this func makes sure the client is connected, meassure the msg length in contrast to the header size and encodes or decodes the msg using utf-8
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[ENCRYPTED MESSAGE FROM CLIENT] {msg}")

            key = bytes(DES_key, 'utf-8')
            #text1 = bytes('HELLO SERVER', 'utf-8')

            des = DES.new(key, DES.MODE_ECB)

            print(f"[UNENCRYPTED MESSAGE FROM CLIENT] {des.decrypt(msg)}")
            

            if connected == False:
                text1 = bytes('Connection Closed!', 'utf-8')
                padded_text = pad(text1)
                encrypted_text = des.encrypt(padded_text)
                conn.send(encrypted_text)
            else:
                text1 = bytes('Hello Client', 'utf-8')
                padded_text = pad(text1)
                encrypted_text = des.encrypt(padded_text)
                conn.send(encrypted_text)
    #close the connection
    conn.close()

#start func where the erver listen for a connection then calls the handle_client passing the client's info
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    print("The shared DES Key is: " + DES_key)
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

print("[STARTING] Server is starting...")

start()
