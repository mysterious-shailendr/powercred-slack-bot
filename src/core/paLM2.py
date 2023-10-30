import json
from .manager import Manager
import datetime
import requests
from cryptography.fernet import Fernet

class paLM2(Manager):
    def __init__(self):
        super().__init__()

    async def get_values(self, training_chunks):
        for key, encrypted_data in training_chunks:
            self.training_chunk.append(Fernet(key).decrypt(encrypted_data).decode('utf-8'))
        
    
    async def req(self, message, user_id):
        date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText?key=AIzaSyAPdx54xpwOYUvgf1fIpikF66vZ6VOwQdI"
        await self.get_values(list(self.raw_training_data["training_chunks"].items()))

        template = f""" 
PreTraining: (About You: (Your name is OptiBot, Today's Date & time is {date_time}.{self.training_chunk[0]}),{self.training_chunk[1]},{self.training_chunk[2]})' 
User: '<@{user_id}>', UserMessage: '{message}'
"""
        data = { "prompt": { "text": template } }
        response = requests.post(url, json=data)

        if 'error' in response.json(): return response.json()['error']['message']
        elif 'candidates' in response.json(): return response.json()['candidates'][0].get('output')
        else: return response.json()