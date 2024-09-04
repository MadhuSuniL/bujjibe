from typing import Generator
import django.conf.urls.static
from base_app.consumers import BaseChatBotAsyncJsonWebsocketConsumer
from base_app.decorators import consumer_method_exception_handler
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .langchain import LargeLanguageModelSourceResponse


class ChatBotConsumer(BaseChatBotAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            await self.send_json({"response": self.user.username})


    # @consumer_method_exception_handler
    async def receive_json(self, content, **kwargs):
        await self.chat_bot_response(content)


    
    async def chat_bot_response(self, query):
        self.source_response = LargeLanguageModelSourceResponse(**query, user = self.user.username)
        await BaseChatBotAsyncJsonWebsocketConsumer.add_new_message_session(query["query"], self.user.username)
        response_generator : Generator = self.source_response.get_response()
        if isinstance(response_generator, str):
            await self.send_json({
                "response": response_generator,
                "user" : self.user.username,
                **query
            })
            await BaseChatBotAsyncJsonWebsocketConsumer.add_new_message_session(response_generator, self.user.username, True)
        else:
            await self.stream_response(response_generator, query)
    
    async def stream_response(self, response_generator : Generator, query):
        full_message = ""
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
            full_message += response
        await BaseChatBotAsyncJsonWebsocketConsumer.add_new_message_session(full_message, self.user.username, is_ai_message=True)    

        await self.send_json({
                "response": "<end>",
                "user" : self.user.username,
                **query
            })


    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
      
        
        