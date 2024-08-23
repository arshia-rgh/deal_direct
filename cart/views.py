from rest_framework import viewsets
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from cart.permissions import IsOwner
from cart.serializers import CartItemSerializer, CartSerializer
from products.mixins import ListCacheMixin, ThrottleMixin


class CartCreateApiView(ThrottleMixin, CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)


class CartRetrieveDestroyAPIView(ThrottleMixin, RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class CartItemViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    cache_key = "cart_items_list"
    queryset = CartItem.objects
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)
