from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        participants = obj.participants.all()
        return request.user in participants
