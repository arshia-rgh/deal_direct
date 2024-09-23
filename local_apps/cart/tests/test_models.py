import pytest

from cart.models import Cart, CartItem
from cart.tests.conftest import test_active_user


@pytest.mark.django_db
class TestCartModel:
    def test_cart_creation(self, test_active_user):
        cart = Cart.objects.create(user=test_active_user)

        assert cart.user.username == "testuser"
        assert cart.products.count() == 0
        assert Cart.objects.filter(id=cart.id).exists()

    def test_creation_invalid_data(self):
        with pytest.raises(Exception):
            cart = Cart.objects.create(user=None)

            assert not Cart.objects.filter(id=cart.id).exists()

    def test_add_products_to_the_cart(self, test_active_user, test_product):
        cart = Cart.objects.create(user=test_active_user)

        cart_item = CartItem.objects.create(
            cart=cart,
            product=test_product,
            quantity=3,
        )

        assert CartItem.objects.filter(id=cart_item.id).exists()
        assert cart_item.cart.user.username == "testuser"
        assert cart_item.quantity == 3
