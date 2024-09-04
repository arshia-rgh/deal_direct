from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from chat.models import ChatRoom
from chat.permissions import IsParticipant
from chat.serializers import ChatRoomSerializer
from products.models import Product
from utils.mixins import ThrottleMixin, LoggingMixin, ListCacheMixin


class ChatRoomViewSet(
    ListCacheMixin, ThrottleMixin, LoggingMixin, viewsets.ModelViewSet
):
    cache_key = "chat_rooms_list"
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated, IsParticipant)

    def perform_create(self, serializer):
        chat_room = serializer.save()

        chat_room.participants.add(self.request.user)
        # add seller of the product to the participants too
        product_id = self.request.data["product"]
        product = Product.objects.get(id=product_id)
        chat_room.participants.add(product.uploaded_by)

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)


class AccessChatRoomView(TemplateView):
    template_name = "chat/chat.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        room_name = self.request.GET.get("room_name")
        data["room_name"] = room_name

        return data
