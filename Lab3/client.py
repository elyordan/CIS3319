from Crypto.Cipher import DES
from Crypto.Hash.MD5 import MD5Hash
import socket
import hashlib
import hmac
import base64





#header is the maximum bit number for the message
HEADER = 64
PORT = 5050
#format in which the bits are encoded or decoded 
FORMAT = 'utf-8'
#message so the server knows that the client gets disconnected so they can connect again
DISCONNECT_MESSAGE = "!DISCONNECTED"
#can use a hard coded ip but because its going to change to another computer is better to get the ip of the server
#SERVER = "127.0.0.1"
SERVER = socket.gethostbyname(socket.gethostname())
#contains the  ip and port
ADDRESS = (SERVER, PORT)

#client will be equal to a socket stream
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect client to the ip and port
client.connect(ADDRESS)

""" def pad(text):
    n = len(text) % 8
    return text + (b' ' * n) """

#check if the msg is 8 bytes long if not them add empty spaces to make it 8
def pad(text):
    if len(text) % 8 != 0:
        toAdd = 8 - len(text) % 8
    return text + (b' ' * toAdd)

# Function that removes the shared DES Key from the file, and returns it as a string
def getKeyFromFile(filename):
    keyFromFile = None

    with open(filename, "r") as key_file:
        keyFromFile = key_file.readline().strip("\r\n")
        
        if(filename =='key.txt'):
            print("The shared DES Key is: " + keyFromFile)
        else:
            print("The shared HMAC Key is: " + keyFromFile)

    return keyFromFile

#func to encrypt message before sending to server

#func to send a message to the server
def send(msg):
    #get the message lenght
    msg_length = len(msg)
    #encode message as a string
    send_length = str(msg_length).encode(FORMAT)
    #take the message lenght and add it to the in order to make it 64 which is the header and its what the server is whathing for
    send_length += b' ' * (HEADER - len(send_length))
    #send the length of the message first
    client.send(send_length)
    #send the real messge econd
    client.send(msg)
    #receive the message from client
    serverMsg = client.recv(2048)

    print(f"[ENCRYPTED MESSAGE FROM SERVER] {serverMsg}")
    print(f"[UNENCRYPTED MESSAGE FROM SERVER] {des.decrypt(serverMsg)}")


key = bytes(getKeyFromFile('key.txt'), 'utf-8')
hmackey = bytes(getKeyFromFile('hmackey.txt'), 'utf-8')
userInput = input()
text1 = bytes(userInput, 'utf-8')

des = DES.new(key, DES.MODE_ECB)

#encrypt the message using hmac first
sign_signature = hmac.new(text1, hmackey, hashlib.md5).hexdigest()
hashmac = hmac.new(hmackey,digestmod=MD5Hash).hexdigest()
finalmsg = hashmac + '' + sign_signature


#padded_text = pad(my_hmac)
encrypted_text = des.encrypt(finalmsg)

print("\n")

print(f"[MESSAGE] {userInput}")
print(f"[MESSAGE HMAC] {sign_signature}")
print(f"[HMAC KEY] {hashmac}")
print(f"[CIPHERTEXT] {finalmsg}")
print(f"[ENCRYPTING CIPHERTEXT USING DES] {encrypted_text}")

print("MESSAGE SENT\n")

send(encrypted_text)

#print(des.decrypt(encrypted_text))

#send a message to disconnect the client
#send(DISCONNECT_MESSAGE)