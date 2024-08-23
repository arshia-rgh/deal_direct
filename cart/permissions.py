from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.

    - Any user can have permission to access the view.
    - Only the owner of the object has permission to perform actions on it.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the request has permission to perform actions on the object.

        Args:
            request (Request): The HTTP request object.
            view (View): The view object.
            obj (Model): The object to check permission against.

        Returns:
            bool: True if the request has permission, False otherwise.
        """

        return obj.user == request.user


class IsOwnerCartItem(IsOwner):
    """
    Custom permission to only allow owners of a cart item to access it.

    This permission class extends the `IsOwner` class to check if the user is the owner of the cart item.
        (obj.user) is meaningless for cart item
    """

    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
