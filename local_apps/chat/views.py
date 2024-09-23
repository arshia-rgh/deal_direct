from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from local_apps.chat.models import ChatRoom
from local_apps.chat.permissions import IsParticipantViewSet, IsParticipantAccess
from local_apps.chat.serializers import ChatRoomSerializer
from local_apps.products.models import Product
from utils.mixins import ThrottleMixin, LoggingMixin, ListCacheMixin


class ChatRoomViewSet(
    ListCacheMixin, ThrottleMixin, LoggingMixin, viewsets.ModelViewSet
):
    cache_key = "chat_rooms_list"
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (IsAuthenticated, IsParticipantViewSet)

    def perform_create(self, serializer):
        chat_room = serializer.save()

        chat_room.participants.add(self.request.user)
        # add seller of the product to the participants too
        product_id = self.request.data["product"]
        product = Product.objects.get(id=product_id)
        chat_room.participants.add(product.uploaded_by)

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)


class AccessChatRoomView(IsParticipantAccess, TemplateView):
    template_name = "chat/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = kwargs.get("room_name")
        context["room_name"] = room_name

        return context
