from apps.cart.permissions import IsOwner


class OrderIsOwnerPermission(IsOwner):
    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
