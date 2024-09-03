from django.urls import path
from .consumers import ChatBotConsumer

urlpatterns = [
    path('ws/chat', ChatBotConsumer.as_asgi())
]