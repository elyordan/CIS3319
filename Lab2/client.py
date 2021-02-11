from Crypto.Cipher import DES
import socket

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

def pad(text):
    n = len(text) % 8
    return text + (b' ' * n)

# Function that removes the shared DES Key from the file, and returns it as a string
def getDESKeyFromFile(filename):
    DES_key = None
    with open(filename, "r") as key_file:
        DES_key = key_file.readline().strip("\r\n")

    print("The shared DES Key is: " + DES_key)
    return DES_key

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


key = bytes(getDESKeyFromFile('key.txt'), 'utf-8')
text1 = bytes(input(), 'utf-8')

des = DES.new(key, DES.MODE_ECB)

padded_text = pad(text1)
encrypted_text = des.encrypt(padded_text)

send(encrypted_text)
#print(des.decrypt(encrypted_text))

#send a message to disconnect the client
#send(DISCONNECT_MESSAGE)