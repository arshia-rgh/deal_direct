from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return True

        if view.action == "create":
            return (
                request.user
                and request.user.is_authenticated
                and request.user.is_active
            )
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ["retrieve"]:
            return True

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.uploaded_by == request.user
        return False
