from channels.generic.websocket import AsyncJsonWebsocketConsumer
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import trim_messages, AIMessage, HumanMessage
from uuid import UUID, uuid4  # Import uuid4 for generating random UUIDs
from collections import OrderedDict

class BaseChatBotAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    __sessions = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def user_connect(self):
        user = self.scope.get('user')
        if user is None:
            await self.close(code=4403)  
            return False
        else:
            await self.accept()
            self.user = self.scope.get('user')
            return True
            
    @classmethod
    def get_session_messages(cls, session_id):
        if session_id not in cls.__sessions:
            cls.__sessions[session_id] = []
        return cls.__sessions.get(session_id)

    @classmethod
    def get_session_and_trim_messages(cls, session_id, model = None):
        if session_id not in cls.__sessions:
            cls.__sessions[session_id] = []
        return cls.trim_messages(cls.__sessions.get(session_id), model)

    @classmethod
    async def add_new_message_session(cls, message, session_id, is_ai_message = False):
        if is_ai_message:
            message = AIMessage(content=message)
        else:
            message = HumanMessage(content=message)
        cls.get_session_messages(session_id).append(message)
    
    @classmethod
    def trim_messages(cls, session, model):
        # trimmer=trim_messages(
        #     max_tokens=1000,
        #     strategy="last",
        #     token_counter=model,
        #     include_system=True,
        #     allow_partial=False,
        #     start_on="human"
        # )
        return session
        return trimmer.invoke(session)

    async def send_msg_and_close(self, msg=''):
        await self.send_json({'detail': msg})
        await self.close()

    @classmethod
    async def generate_random_id(cls):
        # Generates a random UUID and returns it as a string
        return str(uuid4())
