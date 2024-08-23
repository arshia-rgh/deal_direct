from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart, CartItem
from cart.permissions import IsOwner
from cart.serializers import CartSerializer, CartItemSerializer
from products.mixins import ListCacheMixin, ThrottleMixin


class CartViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)
