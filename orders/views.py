from django.http import Http404
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
from utils.mixins import ThrottleMixin
from .permissions import OrderIsOwnerPermission


class OrderCreateAPIView(ThrottleMixin, CreateAPIView):
    """
    API view to create an order.

    This view allows authenticated users to create a new order.
    It uses the `OrderSerializer` to validate and save the order data.
    """

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderPayAPIView(ThrottleMixin, APIView):
    """
    API view to handle order payment.

    This view allows authenticated users to pay for an order.
    It checks if the user has sufficient wallet balance to pay for the order.
    If the payment is successful, it updates the order status and schedules
    a task to delete the cart after 7 days.
    """

    permission_classes = (IsAuthenticated, OrderIsOwnerPermission)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to pay for an order.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response with the payment status.
        """

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
            update_wallet_balance.delay(user.id, -order.total_price)

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


class OrderRetrieveDestroyAPIView(ThrottleMixin, generics.RetrieveDestroyAPIView):
    """
    API view to retrieve or destroy an order.

    This view allows authenticated users to retrieve or delete their order.
    It uses the `OrderSerializer` to serialize the order data.
    """

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, OrderIsOwnerPermission)

    def get_object(self):
        """
        API view to retrieve or destroy an order.

        This view allows authenticated users to retrieve or delete their order.
        It uses the `OrderSerializer` to serialize the order data.
        """

        try:
            return Order.objects.get(cart__user=self.request.user)
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
