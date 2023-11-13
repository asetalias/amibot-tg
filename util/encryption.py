from cryptography.fernet import Fernet
from util.env import KEY


def encrypt(username: int, password: str):
    cipher_suite = Fernet(KEY)
    username = str(username)
    encrypted_username = cipher_suite.encrypt(username.encode())
    enccrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_username.decode(), enccrypted_password.decode()


def decrypt(encrypted_username, encrypted_password):
    cipher_suite = Fernet(KEY)
    decrypted_username = int(cipher_suite.decrypt(encrypted_username).decode())
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_username, decrypted_password
