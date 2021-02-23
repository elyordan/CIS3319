from types import resolve_bases
from Crypto.Cipher import DES
from Crypto.Hash.MD5 import MD5Hash
import socket
import random
import hashlib
import hmac

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
HMAC_key = str(random.randint(10000000,99999999))

#create a new file with the shared keys for the client
def shareKey():
    f = open('key.txt', 'w')
    f.write(DES_key)
    f.close()

    f2 = open('hmackey.txt', 'w')
    f2.write(HMAC_key)
    f2.close()  

shareKey()


""" def pad(text):
    n = len(text) % 8
    return text + (b' ' * n) """

#check if the msg is 8 bytes long if not them add empty spaces to make it 8
def pad(text):
    if len(text) % 8 != 0:
        toAdd = 8 - len(text) % 8
    return text + (b' ' * toAdd)

#server will be equal to a socket stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the server with the address
server.bind(ADDRESS)

#After receiving the client's info this func makes sure the client is connected, meassure the msg length in contrast to the header size and encodes or decodes the msg using utf-8
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    print("\n")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            key = bytes(DES_key, 'utf-8')

            des = DES.new(key, DES.MODE_ECB)
            string = des.decrypt(msg)

            

            #split the ciphertext to only get the hmac key and the encoded text, then decode it
            n = 32
            out = [(string[i:i+n]) for i in range(0, len(string), n)] 
            hexFromClient = out[1].decode()
            hmacFromClient = out[0].decode()
            finalmsg = bytes.fromhex(hexFromClient).decode('utf-8')

            #print all the info received from client
            print("******** NEW MESSAGE FROM CLIENT ******** ")
            print("\n")

            print(f"[MESSAGE] {finalmsg}")
            print(f"[MESSAGE HMAC] {hexFromClient}")
            print(f"[CIPHERTEXT] {des.decrypt(msg).decode()}")
            print(f"[ENCRYPTED DES FROM CLIENT] {msg}")

            #compare hmac for validation then print both for the user to see
            hmackey = bytes(HMAC_key, 'utf-8')
            hmacFromServer = hmac.new(hmackey,digestmod=MD5Hash).hexdigest()

            if(hmacFromClient == hmacFromServer):
                print(f"[HMAC FROM CLIENT] {hmacFromClient}")
                print(f"[HMAC GENERATED] {hmacFromServer}")
                print('HMAC HAS BEEN VERIFIED!')
            else:
                print(f"[HMAC FROM CLIENT] {hmacFromClient}")
                print(f"[HMAC GENERATED] {hmacFromServer}")
                print('HMAC DO NOT MATCH!')
                

            print("\n")

            if connected == False:
                text1 = bytes('Connection Closed!', 'utf-8')
                padded_text = pad(text1)
                encrypted_text = des.encrypt(padded_text)
                conn.send(encrypted_text)
            else:
                text1 = bytes('Hello Client', 'utf-8')
                sign_signature = text1.hex()
                hashmac = hmac.new(hmackey,digestmod=MD5Hash).hexdigest()
                finalmsg = hashmac + '' + sign_signature
                encrypted_text = des.encrypt(finalmsg)
                print(f"[MESSAGE] {text1.decode()}")
                print(f"[MESSAGE HMAC] {sign_signature}")
                print(f"[HMAC KEY] {hashmac}")
                print(f"[CIPHERTEXT] {finalmsg}")
                print(f"[ENCRYPTED DES MESSAGE] {encrypted_text}")
                # padded_text = pad(text1)
                # encrypted_text = des.encrypt(padded_text)
                # print(f"[ENCRYPTING MESSAGE] {'Hello Client'}")
                # print(f"[ENCRYPTED MESSAGE] {encrypted_text}")

                conn.send(encrypted_text)
                print("MESSAGE SENT\n")
    #close the connection
    conn.close()

#start func where the erver listen for a connection then calls the handle_client passing the client's info
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    print("The shared DES Key is: " + DES_key)
    print("The shared HMAC Key is: " + HMAC_key)
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

print("[STARTING] Server is starting...")

start()
