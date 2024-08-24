from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from orders.serializers import OrderSerializer
from products.mixins import ThrottleMixin


class OrderCreateAPIView(ThrottleMixin, CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
