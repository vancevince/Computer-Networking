# Implementation of group chat server app in python. Borrowed much of the
# structure from Professor Srihari Nelakutiti.

# Copyright 2022
# Vincent Kolb-Lugo
# CSCE 416

# Import libraries
from socket import *
from sys import *
from select import *

# Server needs the port number to listen on
if len(argv) != 2:
    print('usage:', argv[0], '<port>')
    exit()

# Make a list of connected clients, sockets
activeClients = []

# Make a list of of clients to write to
#writeToClients = []

# Get the port on which serve should listen
serverPort = int(argv[1])

# Create the server socket
serverSock = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the given port
serverSock.bind(('', serverPort))

# Listen for clients
serverSock.listen()

# Add server socket to list of ACTIVE_CLIENTS

# Wait to receive connection request
print('Chat started. \n Waiting for clients ...')

# No other clients, close the server socket
#serverSock.close() # this line might be too early

# Make a file stream 
clientSockFile = {}
clientName = {}

# Keep receiving and relaying messages from clients to ACTIVE_CLIENTS list
while True:
    
    # Get the reading and writing buffers(?) ready for select
    readableSet, _, _ = select(activeClients + [serverSock], [], [])

    # New connection
    for sock in readableSet:
        
        if sock == serverSock:
            # Handle new connection when received through server_socket
            # clientSock used for writing, clientSockFile used for reading
            clientSock, clientAddr = serverSock.accept()
            clientSockFile[clientSock] = clientSock.makefile()
            
            # get the new clinet's name from the client and store it in a 
            # clientName dictionary w/ clientSock as the key value
            clientName[clientSock] = clientSockFile[clientSock].readline()[:-1]
            print('Client %s has connected' % clientName[clientSock]) 
           
            activeClients.append(clientSock)
            

        else:
            # Get message from client, relay it to others
            # Use the clientSockFile dictionary to identify from who the
            # incoming message is coming from
            if sock in readableSet:
                print('About to read from', clientName[sock])
                # follow TwowaySync Logic
                line = clientSockFile[sock].readline()

                if not line:
                    # removing client from acctive user list and dictionary
                    print('***' + clientName[sock] + ' has left the chat')
                    activeClients.remove(sock)
                    clientSockFile[sock].close()                
                    clientName.pop(sock)
                    clientSockFile.pop(sock)    
                    break

                # Send the line to the other active members of chat
                line = clientName[sock] + '> ' + line
                for client in activeClients:
                    # iterate through active client list to relay message to clients
                    if client != sock:
                        try:
                            client.send(line.encode())
                        except:
                            client.close() # EOF
                            activeClients.remove(client)
