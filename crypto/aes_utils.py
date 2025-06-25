from cryptography.fernet import Fernet
import os

class aes_utils:
    symmetricFile = "symmetric_key_file.txt"

    def __init__(self):
        #Create a txt file for storing the key and store the key inside it. 
        # only create if it doesnt exist
        if not os.path.exists(self.symmetricFile):
            self.createKeyFile()
        # load the key from the text file into the symmetric key
        self.symmetricKey = self.loadKeyFromFile()

    def loadKeyFromFile(self):
        #this method actually returns the key from the text file
        with open(self.symmetricFile, "rb") as file:
            return file.read()
        

    def createKeyFile(self):
        #this method generates a random key and places that key into the text file
        with open(self.symmetricFile, "wb") as file:
            symmetricKey = Fernet.generate_key()
            file.write(symmetricKey)

    def encryptMessage(self, data):
        #this method encrypts the message using the Fernet class's encrypt method and returns the encrypted data
        engine = Fernet(self.symmetricKey) # initiliase the Fernet object with the key used for encryption
        encryptedData = engine.encrypt(data) 
        return encryptedData

    def decryptMessage(self, data):
        # decrypts the message using Fernet class's decrypt method and returns the decrypted data
        engine = Fernet(self.symmetricKey)
        decryptedData = engine.decrypt(data)
        return decryptedData
    