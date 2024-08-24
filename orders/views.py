from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.tasks import update_wallet_balance
from orders.models import Order
from orders.serializers import OrderSerializer
from products.mixins import ThrottleMixin


class OrderCreateAPIView(ThrottleMixin, CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderPayAPIView(ThrottleMixin, APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        order = Order.objects.get(cart__user=user)

        if order and order.total_price <= user.wallet:
            update_wallet_balance.delay(-order.total_price)

            order.status = Order.OrderStatusChoices.sending
            order.save()

            # TODO implement this later

            return Response({"message": "Payment was successful"})
