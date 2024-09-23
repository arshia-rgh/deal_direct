from django.urls import path

from local_apps.chat.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatRoomConsumer.as_asgi()),
]
