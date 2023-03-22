import os
from cryptography.fernet import Fernet

key = os.environ['FERNET_KEY'].encode("utf-8")
cipher_suite = Fernet(key)

class Secure:
    def __init__(self):
        pass
    def encrypt_data(data):
        return cipher_suite.encrypt(data.encode("utf-8"))

    def decrypt_data(encrypted_data):
        return cipher_suite.decrypt(encrypted_data).decode("utf-8")