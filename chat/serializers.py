from rest_framework import serializers

from chat.models import ChatRoom


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"
        read_only_fields = ["id", "created", "modified"]
