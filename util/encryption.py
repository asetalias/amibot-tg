from cryptography.fernet import Fernet
from util.env import KEY

def encrypt(password):
    cipher_suite = Fernet(KEY)
    enccrypted_password = cipher_suite.encrypt(password.encode())
    return enccrypted_password.decode()

def decrypt(encrypted_password):
    cipher_suite = Fernet(KEY)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password