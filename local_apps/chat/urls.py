from django.urls import path, include
from rest_framework.routers import DefaultRouter

from local_apps.chat.views import ChatRoomViewSet, AccessChatRoomView

router = DefaultRouter()

router.register("chat-rooms", ChatRoomViewSet)

app_name = "chats"

urlpatterns = [
    path("", include(router.urls)),
    path("chat/<str:room_name>/", AccessChatRoomView.as_view(), name="access-chat"),
]
