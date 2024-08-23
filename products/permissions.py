from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    - Any authenticated and active user can have permission to access the view.
    - Only the owner of the object has permission to perform update or delete actions.
    """

    def has_permission(self, request, view):
        """
        Check if the request has permission to access the view.

        Args:
            request (Request): The HTTP request object.
            view (View): The view object.

        Returns:
            bool: True if the request has permission, False otherwise.
        """

        return bool(
            request.user and request.user.is_authenticated and request.user.is_active
        )

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
