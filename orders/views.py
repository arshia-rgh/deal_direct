from rest_framework.generics import CreateAPIView

from orders.serializers import OrderSerializer


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderSerializer
