from typing import Generator
import django.conf.urls.static
from base_app.consumers import BaseAsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .langchain import LargeLanguageModelSourceResponse


class ChatBotConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            await self.send_json({"response": self.user.username})


    async def receive_json(self, content, **kwargs):
        await self.chat_bot_response(content)
    
    
    async def chat_bot_response(self, query):
        self.source_response = LargeLanguageModelSourceResponse(**query, user = self.user.username)
        response_generator : Generator = self.source_response.get_response()
        await self.stream_response(response_generator, query)
    
    async def stream_response(self, response_generator : Generator, query):
        await self.send_json({
                "response": '<start>',
                "user" : self.user.username,
                **query
            })
        for response in response_generator:
            await self.send_json({
                "response": response,
                "user" : self.user.username,
                **query
            })
        await self.send_json({
                "response": "<end>",
                "user" : self.user.username,
                **query
            })


    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
      
        
        