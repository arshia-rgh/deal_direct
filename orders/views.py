from rest_framework import generics
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.tasks import update_wallet_balance
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.tasks import delete_cart_after_7_days
from products.mixins import ThrottleMixin


class OrderCreateAPIView(ThrottleMixin, CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderPayAPIView(ThrottleMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            order = Order.objects.get(cart__user=user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found, Create One first "},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.total_price <= user.wallet:
            # payment successfully
            update_wallet_balance.delay(-order.total_price)

            order.status = Order.OrderStatusChoices.sending
            order.save()

            # products delivered successfully
            delete_cart_after_7_days.apply_async(
                (order.id,), countdown=7 * 24 * 60 * 60
            )

            # update all sellers wallet balance
            for item in order.cart.cartitem_set.all():
                item.product.bought_by = request.user
                product_owner = item.product.uploaded_by
                update_wallet_balance(
                    product_owner.id, item.product.price * item.quantity
                )

            return Response(
                {
                    "message": "Payment was successful, Your order will be delivered in 7 days"
                }
            )

        return Response(
            {"error": "Insufficient wallet balance"}, status=status.HTTP_400_BAD_REQUEST
        )


class OrderRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
