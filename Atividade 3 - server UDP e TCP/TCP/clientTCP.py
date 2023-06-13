# clientTCP.py
from socket import *

serverName = 'localhost'
serverPort = 12000

with open('responses.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(line.strip().encode())
    modifiedMessage = clientSocket.recv(1024)
    print('From Server:', modifiedMessage.decode())
    clientSocket.close()
