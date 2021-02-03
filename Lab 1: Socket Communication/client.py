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

#func to send a message to the server
def send(msg):
    #encode the message using utf8 into bytes
    message = msg.encode(FORMAT)
    #get the message lenght
    msg_length = len(message)
    #encode message as a string
    send_length = str(msg_length).encode(FORMAT)
    #take the message lenght and add it to the in order to make it 64 which is the header and its what the server is whathing for
    send_length += b' ' * (HEADER - len(send_length))
    #send the length of the message first
    client.send(send_length)
    #send the real messge econd
    client.send(message)
    #receive the message from client
    print(
        "[MESSAGE FROM SERVER]" 
        + client.recv(2048).decode(FORMAT))

send("Hi server, this is client.")
#send a message to disconnect the client
send(DISCONNECT_MESSAGE)