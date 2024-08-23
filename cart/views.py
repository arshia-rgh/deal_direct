from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from cart.permissions import IsOwner
from cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
