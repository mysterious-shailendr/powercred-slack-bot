# import json
# from cryptography.fernet import Fernet

# key = Fernet.generate_key()

# cipher = Fernet(key)

# text = """..."""
# data = text.encode('utf-8')

# encrypted_data = cipher.encrypt(data)

# print("key: ",key)
# print("encrypted data: ",encrypted_data)


from cryptography.fernet import Fernet

key = b'9gFeqTMuwit95ZVRnF0CtNoWgpwnyHC4NiZ8xfJDmZU='

encrypted_data = "gAAAAABlPluIdbAKmuIQ2H_6dP4a-C7ivBqLNsb_NxXaa6eYjYNKnbnuDHv6swnyQMnJrC08jqb2wnqFRl-ErZcNHhjlcwpO5Q=="
cipher = Fernet(key)
decrypted_data = cipher.decrypt(encrypted_data)
text = decrypted_data.decode('utf-8')
print(text)


# class CypherLib:
#     def __init__(self, key):
#         self.key = key
#         self.cipher = Fernet(key)

#     def encrypt(self, data):
#         encrypted_data = self.cipher.encrypt(data)
#         return encrypted_data

#     def decrypt(self, encrypted_data):
#         decrypted_data = self.cipher.decrypt(encrypted_data)
#         return decrypted_data

import json


path = './powercred.json'
with open(path, 'r') as file:
    data = json.load(file)
    training_chunks = data["training_chunks"]
    training_chunks = list(training_chunks.items())