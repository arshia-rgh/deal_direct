import pytest

from local_apps.orders.models import Order


@pytest.mark.django_db
class TestOrderModel:
    def test_order_creation(self, test_cart):
        order = Order.objects.create(cart=test_cart)

        assert len(Order.objects.all()) == 1
        assert order.user == test_cart.user
        assert order.products == [item.product for item in test_cart.cartitem_set.all()]
        assert order.status == Order.OrderStatusChoices.waiting_for_payment
        assert order.total_price == sum(
            item.product.price * item.quantity for item in test_cart.cartitem_set.all()
        )

    def test_order_creation_invalid_data(self):
        with pytest.raises(Exception):
            Order.objects.create(cart="invalid cart")

            assert len(Order.objects.all()) == 0

    def test_update_order(self, test_cart):
        order = Order.objects.create(cart=test_cart)

        assert order.status == Order.OrderStatusChoices.waiting_for_payment

        order.status = "C"
        order.save()

        order.refresh_from_db()

        assert order.status == Order.OrderStatusChoices.completed

    def test_delete_order(self, test_cart):
        order = Order.objects.create(cart=test_cart)

        assert len(Order.objects.all()) == 1

        order.delete()

        assert len(Order.objects.all()) == 0
