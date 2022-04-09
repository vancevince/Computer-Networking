# Implementation of a group chat CLIENT in python
# Copyright 2021
# Vincent Kolb-Lugo
# CSCE 416

# get the libraries
from socket import *
from sys import *
from select import *

# Client needs server's contact information
if len(argv) != 4:
    print("Usage:", argv[0], "<server name> <server port> <user name>")
    exit()

# Get server's whereabouts
serverName = argv[1]
serverPort = int(argv[2])
userName = argv[3]


# Create the socket
sock = socket(AF_INET, SOCK_STREAM)

# Connect to the server
sock.connect((serverName, serverPort))
print(f"Connected to server at ('{serverName}', '{serverPort}')")

# Send the user's name to the server
sock.send(userName.encode())
sock.send('\n'.encode())

# Make a file stream out of the socket
sockFile = sock.makefile(mode='r')

# Make a list of inputs to watch for
inputSet = [stdin, sockFile]



# Keep sending and recceiving message from the server
while True:
     
    # Wait for a message from keyboard or socket
    readableSet, x, x = select(inputSet, [], [])

    # Check if there is a message from the keyboard
    if stdin in readableSet:
        # Read a line from the keyboard
        line = stdin.readline()

        # If EOF --> client wants to close the connection 
        if not line:
            print('*** Client closing connection')
            break

        # Send the line to client
        sock.send(line.encode())

    # Check if there is a message from the socket
    if sockFile in readableSet:
        # Read a messafe from the client
        line = sockFile.readline()

        # if EOF --> client closed the connection
        if not line:
            print('*** Server closed connection')
            break
        
        # this might need to change to be able to display name of sender, not server
        # Display the line
        print(line, end='')

# Close the connection
sockFile.close()
sock.close()
