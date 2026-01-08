from django.urls import path
from . import consumers

# Список маршрутов для WebSocket-соединений.
websocket_urlpatterns = [
    path('ws/chat_rooms/<room_name>/', consumers.ChatConsumer.as_asgi()),
]