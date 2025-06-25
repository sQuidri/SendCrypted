# Establish a TCP connection among the client and server.
# This file will handle the client side connection, so connecting to the server using socket's IP and port number

import socket #
import os
from crypto.aes_utils import aes_utils


class client_net:
    def __init__(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.serverSocketAddress = (serverIP, serverPort)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Af_inet is for ipv4 addresses and Sock_stream is for TCP connections
        self.symmetricKeyUtils = aes_utils()
    
    def connectToServerSocket(self):
        # connect to the server socket through .connect()
        self.clientSocket.connect(self.serverSocketAddress)
    
    def sendingFilesToServer(self, filePath):

        #sending the file name
        fileName = os.path.basename(filePath)
        self.clientSocket.sendall((fileName + '\n').encode())

        #sending the file size
        fileSize = os.path.getsize(filePath)
        self.clientSocket.sendall((str(fileSize) + '\n').encode())

        #loop that reads the file in chunks and sends one chunk at a time
        chunksSize = 1024
        with open(filePath, 'rb') as file:
            while True:
                data = file.read(chunksSize)
                encrypted_data = self.encryptData(data)
                if not encrypted_data:
                    break
                self.clientSocket.sendall(encrypted_data)

    def encryptData(self, data):
        return self.symmetricKeyUtils.encryptMessage(data)
 

