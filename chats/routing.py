from django.urls import re_path, path
from chats import consumers

websocket_urlpatterns = [
    path("chats/<str:room_name>/", consumers.ChatRoomConsumer.as_asgi())
]