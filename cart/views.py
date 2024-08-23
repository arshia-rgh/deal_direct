from rest_framework import viewsets
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem, Cart
from cart.permissions import IsOwner
from cart.serializers import CartItemSerializer, CartSerializer
from products.mixins import ListCacheMixin, ThrottleMixin


class CartCreateApiView(ThrottleMixin, CreateAPIView):
    """
    API view to create a new cart.

    This view allows authenticated users to create a new cart.
    It uses the `CartSerializer` to handle serialization and deserialization.
    """

    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class CartRetrieveDestroyAPIView(ThrottleMixin, RetrieveDestroyAPIView):
    """
    API view to retrieve or destroy a cart.

    This view allows authenticated users to retrieve or delete their own cart.
    It uses the `CartSerializer` to handle serialization and deserialization.
    """

    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        """
        Retrieve the cart for the current user.

        Returns:
            Cart: The cart instance for the current user.
        """

        return Cart.objects.get(user=self.request.user)


class CartItemViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing cart items.

    This view allows authenticated users to perform CRUD operations on their cart items.
    It uses the `CartItemSerializer` to handle serialization and deserialization.
    """

    cache_key = "cart_items_list"
    queryset = CartItem.objects
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        """
        Retrieve the cart items for the current user's cart.

        Returns:
            QuerySet: The queryset of cart items for the current user's cart.
        """

        return CartItem.objects.filter(cart=self.request.user.cart)
