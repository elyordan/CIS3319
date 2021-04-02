
import socket
import sys
import ipaddress
import time
import datetime
import pickle

# Constant values provided
host = '127.0.0.1'
idC = "CIS3319USERID"
idV = "CIS3319SERVERID"
idTGS = "CIS3319TGSID"
portS = 8000
portV = 8002
lifetime2 = 60
lifetime4 = 86400
keyV = 0
keyTGS = 0

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\nSocket successfully created\n")

# This is the AS
s.connect((host, portS))
print("AS_server Says: " + pickle.loads(s.recv(1024)))

timestamp = datetime.datetime.now
message = [idC, idTGS, timestamp]

s.send(pickle.dumps(message))
print("Requesting AS_TGT_Server for TGT!")
returnMsg = pickle.loads(s.recv(1024))
tgt = returnMsg[4]
print("TGT received from server!\n")

# TGS communication
message = [idV, tgt]

s.send(pickle.dumps(message))
print("Requesting AS_TGT_Server for service ticket!")
returnMsg = pickle.loads(s.recv(1024))
print("Service ticket received from server!\n")

# new socket setup
s.close
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created\n")

# Service communication
s.connect((host, portV))
print(pickle.loads(s.recv(1024)))

s.send(pickle.dumps(returnMsg[3]))
print("Requesting connection to V_Server for service!")
returnMsg = pickle.loads(s.recv(1024))
print("Service authenticated by V_Server!\n")

# end of client
s.close()
exit(0)
