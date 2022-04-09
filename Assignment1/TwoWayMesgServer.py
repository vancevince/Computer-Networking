# Vincent Kolb-Lugo
# Copyright 2022
# Framework of assignment borrowed from Srihari Nelakuditi for CSCE 416
# 
# Assignment 1: Implement a simple two-way messaging application using
# a TCP socket connection.

# Import socket related methods
from socket import *

# Import argv related methods
from sys import *


# Server needs the port number to listen on
if len(argv) != 2:
    print('usage:', argv[0], '<port>')
    exit()

# Get the port on which server should listen */
serverPort = int(argv[1])

# Create the server socket
serverSock = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the given port
serverSock.bind(('', serverPort))

# Set the server for listening */
serverSock.listen()

# Wait to receive a connection request
print('Waiting for a client ...')
clientSock, clientAddr = serverSock.accept()
print('Connected to a client at', clientAddr)

serverSock.close()

while True:
    # receive message from client machine
    cl_message = clientSock.recv(1024)
    if not cl_message:
        print('Client closed the connection')
        clientSock.close()
        break
    print('Client:', cl_message.decode())
    
    # send message from server to client
    try:
        outgoing_message = input('> ')
    except EOFError as e:
        print('Server closed the connection')
        clientSock.close()
        break
    # New code
    if not outgoing_message:
        print('Server closed the connection')
        clientSock.close()
        break
    try:
        clientSock.send(outgoing_message.encode())
    except ConnectionResetError as e:
        break
