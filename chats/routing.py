from django.urls import re_path, path
from chats import consumers

websocket_urlpatterns = [
    path("", consumers.ChatRoomConsumer.as_asgi())
]