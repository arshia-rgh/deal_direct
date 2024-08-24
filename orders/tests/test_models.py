import pytest

from orders.models import Order


@pytest.mark.django_db
class TestOrderModel:
    def test_order_creation(self, test_cart):
        order = Order.objects.create(cart=test_cart)

        assert len(Order.objects.all()) == 1
        assert order.user == test_cart.user
        assert order.products == [item.product for item in test_cart.cartitem_set.all()]
        assert order.status == Order.OrderStatusChoices.pending
        assert order.total_price == sum(
            item.product.price * item.quantity for item in test_cart.cartitem_set.all()
        )
