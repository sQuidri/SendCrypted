import rsa
from network.server_net import server_net

class rsa_utils:

    def __init__(self) :
        server = server_net() 
        self.serverPublicKey = server.keyExchange()

    def encryption(self, symmetricKeyToEncrypt):
        #This will encrypt the symmetric key with the server public key
        encryptedKey = rsa.encrypt(symmetricKeyToEncrypt, self.serverPublicKey)
        return encryptedKey