from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart, CartItem
from cart.permissions import IsOwner
from cart.serializers import CartSerializer, CartItemSerializer
from products.mixins import ListCacheMixin, ThrottleMixin


class CartViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class CartItemViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        return CartItem.objects.get(cart=self.request.user.cart)
