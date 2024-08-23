from rest_framework.permissions import BasePermission


class IsAuthenticatedAndActive(BasePermission):
    """
    Custom permission to only allow authenticated and active users to access the view.

    - Only authenticated and active users are granted permission.
    """

    def has_permission(self, request, view):
        """
        Check if the request has permission to perform the action.

        Args:
            request (Request): The HTTP request object.
            view (View): The view object.

        Returns:
            bool: True if the user is authenticated and active, False otherwise.
        """
        return bool(
            request.user and request.user.is_authenticated and request.user.is_active
        )
