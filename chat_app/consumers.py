from typing import Generator
import django.conf.urls.static
from base_app.consumers import BaseChatBotAsyncJsonWebsocketConsumer
from base_app.decorators import consumer_method_exception_handler
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .langchain import LargeLanguageModelSourceResponse, PretrainedPdfFileSourceResponse, WebSourceResponse


class ChatBotConsumer(BaseChatBotAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            pass
            # await self.chat_bot_response({
            #                               "query" : "Hi",
            #                               "topic" : None,
            #                               "model" : "gemma2-9b-it",
            #                               })


    # @consumer_method_exception_handler
    async def receive_json(self, content, **kwargs):
        print(content)
        await self.chat_bot_response(content)


    
    async def chat_bot_response(self, query):
        query_meta = query
        query = query_meta.get('query', 'Hi!')
        topic = query_meta.get('topic', 'all')
        source = query_meta.get('source', {})
        source_type = source.get('type', 'llm')
        choice = source.get('source', 'gemma2-9b-it')

        user = self.user.username
        self.source_response = None

        if source_type == 'llm':
            self.source_response = LargeLanguageModelSourceResponse(
                query, topic, choice, user)
        elif source_type == 'web':
            self.source_response = WebSourceResponse(
                query, topic, choice, user)
        else:
            self.source_response = PretrainedPdfFileSourceResponse(
                query, topic, user)
        
        await BaseChatBotAsyncJsonWebsocketConsumer.add_new_message_session(query, self.user.username)
        response_generator : Generator | str = self.source_response.get_response()
        uuid : str = await BaseChatBotAsyncJsonWebsocketConsumer.generate_random_id()
        await self.stream_response(response_generator, query_meta, uuid)
    
    async def stream_response(self, response_generator, query_meta, uuid, success = True):
        full_message = ""
        await self.send_json({
                "id" : uuid,
                "content": '<start>',
                "user" : self.user.username,
                "success" : success,
                **query_meta
            })
        
        for response in response_generator:
            await self.send_json({
                "id" : uuid,
                "content": response,
                "user" : self.user.username,
                "success" : success,
                **query_meta
            })
            full_message += response
        await BaseChatBotAsyncJsonWebsocketConsumer.add_new_message_session(full_message, self.user.username, is_ai_message=True)    

        await self.send_json({
                "id" : uuid,
                "content": "<end>",
                "user" : self.user.username,
                "success" : success,
                **query_meta
            })


    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
      
        
        