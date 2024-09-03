import django.conf.urls.static
from base_app.consumers import BaseAsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class ChatBotConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            pass

    async def receive_json(self, content, **kwargs):
        pass


    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
      
        
        