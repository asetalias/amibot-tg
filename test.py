from util.encryption import encrypt, decrypt

password = "Achintya"

encrypted_password = encrypt(password)
print(encrypted_password)

decrypted_password = decrypt(encrypted_password)
print(decrypted_password)
