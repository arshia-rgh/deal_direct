from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat.views import ChatRoomViewSet

router = DefaultRouter()

router.register("chat-rooms", ChatRoomViewSet)
app_name = "chats"
urlpatterns = [path("", include(router.urls))]
