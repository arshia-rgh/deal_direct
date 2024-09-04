from rest_framework.permissions import BasePermission


class IsParticipantViewSet(BasePermission):
    def has_object_permission(self, request, view, obj):
        participants = obj.participants.all()
        return request.user in participants


class IsParticipantAccess(BasePermission):
    def has_permission(self, request, view):
        room_name = request.GET.get("room_name")
        if not room_name:
            return False
        return (
            request.user.is_authenticated
            and request.user.chatroom_set.filter(name=room_name).exists()
        )
