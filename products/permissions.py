from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow any user to view the list or retrieve a product

        if view.action in ["list", "retrieve"]:
            return True

        # Allow authenticated users to create a product

        if view.action in ["create", "update", "partial_update", "destroy"]:
            return (
                request.user
                and request.user.is_authenticated
                and request.user.is_active
            )

        return False

    def has_object_permission(self, request, view, obj):
        # Allow any user to view the product details

        if view.action in ["retrieve"]:
            return True

        # Allow only the owner to update or delete the product

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.uploaded_by == request.user
        return False


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_staff
        )
