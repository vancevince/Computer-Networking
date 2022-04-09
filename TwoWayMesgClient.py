# Vincent Kolb-Lugo
# Copyright 2022
# Framework of assignment borrowed from Srihari Nelakuditi for CSCE 416
#
# Assignment 1: Implement a simple two-way messaging application using
# a TCP socket connection

# Import socket related methods
from socket import *

# Import argv related methods
from sys import *


# Client needs server's contact information
if len(argv) != 3:
    print("usage:", argv[0], "<server name> <server port>")
    exit()

# Get server's whereabouts
serverName = argv[1]
serverPort = int(argv[2])

# Create a socket
sock = socket(AF_INET, SOCK_STREAM)

# Connect to the server
sock.connect((serverName, serverPort))
print(f"Connected to server at ('{serverName}', '{serverPort}')");

# find a way to gracefully exit
while True:
    # get input from client user and send to server
    try:
        client_message = input('> ')
    except EOFError as e:
        print('Closing connection')
        sock.close()
        break
    if not client_message:
        break
    sock.send(client_message.encode())

    # receive message from server and display it to console
    server_message = sock.recv(1024)
    if not server_message:
        break
    print('Server:', server_message.decode())

sock.close()