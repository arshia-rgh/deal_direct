from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer
from utils.mixins import ThrottleMixin, LoggingMixin, ListCacheMixin


class ChatRoomViewSet(
    ListCacheMixin, ThrottleMixin, LoggingMixin, viewsets.ModelViewSet
):
    cache_key = "chat_rooms_list"
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        chat_room = serializer.save()

        chat_room.add_participants(self.request.user)

        chat_room.save()
