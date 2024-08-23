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
    """
    Custom permission to only allow admin users to edit objects.

    - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for any user.
    - Non-safe methods (POST, PUT, DELETE) are allowed only for admin users.
    """

    def has_permission(self, request, view):
        """
        Check if the request has permission to perform the action.

        Args:
            request (Request): The HTTP request object.
            view (View): The view object.

        Returns:
            bool: True if the request has permission, False otherwise.
        """
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_staff
        )
