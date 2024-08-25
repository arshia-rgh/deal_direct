import pytest
from django.urls import reverse

from accounts.tasks import update_wallet_balance
from accounts.tests.conftest import api_client
from cart.models import Cart
from orders.models import Order
from orders.tasks import delete_cart_after_7_days


@pytest.mark.django_db
class TestOrderCreateAPIView:
    def test_create_order_successfully(self, api_client, test_active_user, test_cart):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(reverse("orders:order-create"))

        assert response.status_code == 201

        assert response.data["cart"] == test_cart.id
        assert response.data["status"] == "W"

    def test_create_user_with_no_cart(self, api_client, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.post(reverse("orders:order-create"))
        print(response.data)

        assert response.status_code == 400

    def test_unauthenticated_user_cannot_create_order(self, api_client):
        response = api_client.post(reverse("orders:order-create"))

        assert response.status_code == 401

    def test_user_cannot_create_order_if_order_exists(
        self, api_client, test_active_user, test_cart
    ):
        api_client.force_authenticate(test_active_user)

        Order.objects.create(cart=test_cart)

        response = api_client.post(reverse("orders:order-create"))

        assert response.status_code == 400


@pytest.mark.django_db
class TestOrderPayAPIView:
    def test_pay_successfully(self, api_client, test_active_user, test_order):
        test_active_user.wallet = 90.00
        test_active_user.save()

        assert test_order.total_price == 80.00

        api_client.force_authenticate(test_active_user)

        response = api_client.get(reverse("orders:order-pay"))

        assert response.status_code == 200
        assert (
            response.data["message"]
            == "Payment was successful, Your order will be delivered in 7 days"
        )

        # call update balance manually
        update_wallet_balance(test_active_user.id, -test_order.total_price)

        test_order.refresh_from_db()
        test_active_user.refresh_from_db()

        assert test_active_user.wallet == 10.00
        assert test_order.status == Order.OrderStatusChoices.sending

        # manually call the task (here will be done now no need 7 days to test)
        delete_cart_after_7_days(order_id=test_order.id)
        test_order.refresh_from_db()

        assert test_order.cart is None
        assert test_order.status == "C"
        assert not Cart.objects.filter(user=test_active_user).exists()

    def test_pay_without_any_order_created(self, api_client, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.get(reverse("orders:order-pay"))

        assert response.status_code == 404
        assert response.data["error"] == "Order not found, Create One first "

    def test_pay_with_insufficient_wallet_balance(
        self, api_client, test_active_user, test_order
    ):
        test_active_user.wallet = 70.00
        test_active_user.save()

        assert test_order.total_price == 80.00

        api_client.force_authenticate(test_active_user)

        response = api_client.get(reverse("orders:order-pay"))

        assert response.status_code == 400
        assert response.data["error"] == "Insufficient wallet balance"


@pytest.mark.django_db
class TestOrderRetrieveDestroyAPIView:
    def test_delete_order_successfully(self, api_client, test_order, test_active_user):
        api_client.force_authenticate(test_active_user)

        response = api_client.delete(reverse("orders:order-detail"))

        assert response.status_code == 204
        assert not Order.objects.filter(id=test_order.id).exists()
