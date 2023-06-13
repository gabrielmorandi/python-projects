from socket import *

serverName = 'localhost'
serverPort = 12000
client = socket(AF_INET, SOCK_DGRAM)

responses = ["1;5;VVFFV", "2;4;VVVV"]

for message in responses:
  messageBytes = message.encode("utf-8")
  client.sendto(messageBytes, (serverName, serverPort))
  modifiedMessage, serverAddress = client.recvfrom(2048)
  print('From Server: ', modifiedMessage.decode())

client.close()