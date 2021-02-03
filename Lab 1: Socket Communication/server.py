import socket

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
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[MESSAGE FROM CLIENT] {msg}")

            if connected == False:
                conn.send("Connection Closed!".encode(FORMAT))
            else:
                conn.send("Hello, nice to meet you.".encode(FORMAT))
    #close the connection
    conn.close()

#start func where the erver listen for a connection then calls the handle_client passing the client's info
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

print("[STARTING] Server is starting...")
start()
