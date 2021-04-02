import socket
import pickle

# Constant values provided
host = '127.0.0.1'
portV = 8002
lifetime4 = 86400
keyV = 0

# Create the socket and set it up for connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\nSocket successfully created")

# bind the socket
s.bind((host, portV))

# listen for connection  and accept a connection from client
s.listen(5)
c, addr = s.accept()
print("Client successfully conected!")
c.send(pickle.dumps("Connection Acknowldged!\n"))

# client communication(V)
request = pickle.loads(c.recv(1024))
time_stamp = request[3]
c.send(pickle.dumps(time_stamp))

# end of service
s.close
exit(0)
