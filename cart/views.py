from rest_framework import viewsets
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from cart.permissions import IsOwner
from cart.serializers import CartItemSerializer
from products.mixins import ListCacheMixin, ThrottleMixin


class CartCreateApiView(CreateAPIView):
    pass


class CartRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    pass


class CartItemViewSet(ListCacheMixin, ThrottleMixin, viewsets.ModelViewSet):
    cache_key = "cart_items_list"
    queryset = CartItem.objects
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.request.user.cart)
