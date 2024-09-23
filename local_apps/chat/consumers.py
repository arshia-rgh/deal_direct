import json
import re

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

from local_apps.chat.models import ChatRoom


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.sanitize_room_name(self.room_name)}"

        try:
            self.room = await ChatRoom.objects.aget(name=self.room_name)
        except ChatRoom.DoesNotExist:
            raise DenyConnection("Room does not exist")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"].username

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "username": username},
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    @staticmethod
    def sanitize_room_name(room_name):
        return re.sub(r"[^a-zA-Z0-9\-_\.]", "_", room_name)[:100]
