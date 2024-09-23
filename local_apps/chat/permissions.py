from django.contrib.auth.mixins import AccessMixin
from rest_framework.permissions import BasePermission


class IsParticipantViewSet(BasePermission):
    def has_object_permission(self, request, view, obj):
        participants = obj.participants.all()
        return request.user in participants


# Django type permission ( for AccessChatRoomView that is a Django View)
class IsParticipantAccess(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        room_name = kwargs.get("room_name")
        if not room_name:
            return self.handle_no_permission()
        if (
            not request.user.is_authenticated
            or not request.user.rooms.filter(name=room_name).exists()
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
