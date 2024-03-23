from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import *
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.my_username = self.scope['user'].username
        # print(self.my_username)
        
        await self.channel_layer.group_add(
            self.my_username,
            self.channel_name  
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.my_username,
            self.channel_name
        )

    async def receive(self, text_data):
        data  = json.loads(text_data)
        # print(type(data))
        await self.channel_layer.group_send(
                self.my_username,
                {
                    'type': 'chat.message',  # Fix the type name
                    'message': data['message'],
                    'count':0
                    
                }
            )
    async def chat_message(self, event):
        message = event['message']
        count = event['count']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'count':count
            
        }))

        
